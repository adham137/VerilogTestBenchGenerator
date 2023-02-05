import random
import re

inputNames = []

#if design input contains 'clk' , generate clock
def clock_generation(inputs):
    s = ""
    for inp in inputs:
        if("clk" in inp):
           s = "initial\n    begin\n    clk = 1'b0;\n    repeat(1000)\n        begin\n        #20\n        clk = ~clk;\n        end\n    end"
 
    return s     
 
 #generate directed and randomized stimulus
 
def insertStimulus():
    sizes = [] #array containing size (no. of bits) of each input
    
    for sInp in inputsNames:
        sizes.append(getSize(sInp))
        inputNames.append((sInp.split(" ")[-1]))
    
    myStr = ""
    
    
    myStr += "//directed test cases \n    "
    for i in range(3):
        for name in inputNames:
            if(name == "clk"):
                continue
            myStr += f"{name} = {getBinaryNum(sizes[inputNames.index(name)])}; \n    "  #call getBinaryNum function to generate a binary number based on the size of input
        myStr += "\n    #20\n\n    "
        
        
    myStr += "//randomized test cases \n    "    
    for i in range(4):
        for name in inputNames:
            if(name == "clk"):
                continue
            myStr += f"{name} = $urandom%{pow(2,sizes[inputNames.index(name)])+1}; \n    " #generate stimulus using verilog function $urandom % (maximum number the input can reach) 
        myStr += "\n    #20\n\n    "    
    return myStr 
    
#get size of each input    
def getSize(sInp):
    if(sInp.split()[-2][0] == '['):
        #this is if it is not size 1
        a = int(sInp.split()[-2][1]) - int(sInp.split()[-2][3])
        return abs(a) + 1
    #this is if a size is not defined
    return 0
    
#generate a binary number based on size of an input 
#for example if size is 3-bits thus output can be 3'b011
def getBinaryNum(size):
    str=""
    if(size==0):
        str +=f"1'b{random.randint(0,1)}"
        return str
   
    str += f"{size}'b"
    for i in range(size):
        str += f"{random.randint(0,1)}"
    return str
    
#generate stimulus based on condtions ensuring full branch covering    
def stimulusForIfConditions(module):
    str = "//testing condtional statements\n    "
    if(checkForIf(module) == False):
        return str
    condtions = condtionsInIf(module)
    
    
    i=1
    for condition in condtions:
        str += f"//condition no.{i}\n    "
        if(condition in inputNames):
            str += f"{condition} = 1'b1\n    "
            for input in inputNames:
                if(input == condition or input == "clk"):
                    continue
                else:
                    str += f"{input} = 1'b0\n    "
        else:
            input = condition.split()[0]
            operator = condition.split()[1]
            term = condition.split()[2]
            str += f"{input} = {binaryGenerator(operator,term)}\n    "
        str += "\n    #20\n\n    "            
        i += 1 
    return str 
    
#checks for any conditional statements in code    
def checkForIf(module):
    variables=[]
    
    lines = module.splitlines()
    for line in lines:
        if(("if" in line ) or ("elseif" in line ) or ("case" in line )):
            return True
    return False
    
#gets the condition(s) inside condtional statements    
def condtionsInIf(module):
    condtions = []
    
    lines = module.splitlines()
    for line in lines:
        if(not('(' in line)): continue
    
        line = line.strip()
        operator = line.split("(")[0]
        if(operator=="if" or operator=="elseif" or operator=="case"):
            condtion = line.split("(")[1][:-1]
            if(not (condtion in condtions)):
                condtions.append(condtion)
    #print(condtions)
    return condtions
    
#genrates a term that satisfies the condition inside conditional statements    
def binaryGenerator(operator , term):
    if((operator == "==")or(operator == "<=")or(operator == ">=")):
        return term
    newTerm =""    
    if(operator == '<'):
        for i in range(len(term)):
            if(term[i]=='1'):
                newTerm += '0'
            else:
                newTerm += term[i]
    else:
        for i in range(len(term)):
            if(term[i]=='0'):
                newTerm += '1'
            else:
                newTerm += term[i]
    return newTerm       
    
# generates $monitor statements to display variables
def insertMonitor():
    spec_inputs = []
    sizes = []
    for sInp in inputsNames:
        sizes.append(getSize(sInp))
        spec_inputs.append(sInp.split(" ")[-1])
    for input in spec_inputs:
        if(input == "clk"):
            sizes.pop(spec_inputs.index(input))
            spec_inputs.remove(input)
    myStr = ""
    num = random.randrange(0 , len(spec_inputs), 1)
    if(sizes[num] == 0):
        sizes[num] += 1
    myStr += f"""$monitor("{spec_inputs[num]} = %{sizes[num]}b", {spec_inputs[num]})"""
    return myStr 
    
    
def get_ports(module):
    ports = module.split(";")[0].split("\n")[2:-2]
    return ports
 
def get_ports_str(module):
    ports = module.split(";")[0].split("\n")[2:-2]
    return "\n".join(ports)
 

def parsed_ports_str(ports : str):
    return ports.replace("wire", "").replace("reg", "").replace("input", "reg").replace("output", "wire").replace(",", ";").replace("\t", " ") +";"
    
def get_inputs(module):
        inp = []
        module = module.split(';')
        operation = module[0]
        operation = operation.strip(" ")
        operation = ' '.join(operation.split())
        operation = operation[6:]
        operation = operation.strip(" ")
        p1 = operation.find('(')
        p2 = operation.find(')')
        operation = operation[p1 + 1:p2]
        operation = operation.strip(" ")
        operation = operation.split(",")
        inputs = []
        outputs = []
        for i in range(len(operation)):
            operation[i] = operation[i].strip(" ")
            ans = re.findall("([^\s]+)", operation[i])
            type = ans[0]
            ans = ans[1:]
            rest = ""
            for e in ans:
                rest = rest + e + " "
            if type == "input":
                inputs.append(rest.strip(" "))
            else:
                outputs.append(rest.strip(" "))
              
        return inputs
        
def get_outputs(module):
        module = module.split(';')
        operation = module[0]
        operation = operation.strip(" ")
        operation = ' '.join(operation.split())
        operation = operation[6:]
        operation = operation.strip(" ")
        p1 = operation.find('(')
        p2 = operation.find(')')
        operation = operation[p1 + 1:p2]
        operation = operation.strip(" ")
        operation = operation.split(",")
        inputs = []
        outputs = []
        for i in range(len(operation)):
            operation[i] = operation[i].strip(" ")
            ans = re.findall("([^\s]+)", operation[i])
            type = ans[0]
            ans = ans[1:]
            rest = ""
            for e in ans:
                rest = rest + e + " "
            if type == "input":
                inputs.append(rest.strip(" "))
            else:
                outputs.append(rest.strip(" "))
       
        return outputs
 
 #ensures that all inputs are registers 
def parsed_inputs(inputs):
    s = ""
    for inp in inputs:
        replacedStr = inp.replace("wire ", "")
        replacedStr = replacedStr.replace("reg ", "")
        s+= f"reg {replacedStr};\n"
        inputs[inputs.index(inp)] = "reg "+replacedStr
    return s
    
#ensures that all outputs are wires
def parsed_outputs(outputs):
    s = ""
    for out in outputs:
        replacedStr = out.replace("wire ", "")
        replacedStr = replacedStr.replace("reg ", "")
        s+= f"wire {replacedStr};\n"
        outputs[outputs.index(out)] = "wire "+replacedStr
    return s 

def parsed_instantiations(inputs):
    s = ""
    for inp in inputs:
        list1 = inp.split(" ")
        inputName = list1[len(list1)-1]
        s+= f"        .{inputName}({inputName}),\n"
    s = s[0:len(s)-2]
    return s
 
 
design = open("testing.txt").read()
 
module_name = design.split()[1]
 
ports = get_ports(design)
 
ports2 = get_ports_str(design)
parsed2 = parsed_ports_str(ports2)


inputsNames = get_inputs(design)
outputsNames = get_outputs(design)


parsed_instantiations = parsed_instantiations(inputsNames+outputsNames)

 
inputs = parsed_inputs(inputsNames)
#print(inputsNames) #with reg and size
outputs = parsed_outputs(outputsNames)
#print(outputsNames)
stim = insertStimulus()
ifStimulus = stimulusForIfConditions(design)
 
out = f"""module {module_name}_tb ();
{inputs}
{outputs}

{clock_generation(inputsNames)}

intial 
    begin
    {insertMonitor()}
    end
    
initial
    begin
    $dumpfile("{module_name}.vcd");
    $dumpvars ;
    
    {ifStimulus}
    
    {stim}
 
    $finish;
    end
 
    {module_name} DUT (
{parsed_instantiations}
    );
endmodule
"""
print(out)