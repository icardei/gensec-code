# Name: DecompileMainFunctions.py
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor

def decompile_functions(program):
    decompiler = DecompInterface()
    decompiler.openProgram(program)
    monitor = ConsoleTaskMonitor()

    # Loop through all functions
    function_manager = program.getFunctionManager()
    functions = function_manager.getFunctions(True)  # True to iterate forward
    for function in functions:
        # Check if function name starts with 'main'
        if function.getName().startswith("main"):
            results = decompiler.decompileFunction(function, 0, monitor)
            if results.decompileCompleted():
                print("Decompiled_Main: \n{}".format(results.getDecompiledFunction().getC()))
            else:
                print("Failed to decompile {}".format(function.getName()))

decompile_functions(currentProgram)

