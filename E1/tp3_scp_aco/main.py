import clsACOSCP as ACOSCP 
#reload(ACOSCP)


if __name__=='__main__':
        
        instanceName='scp41.txt'

        instanceDir='C:\\Users\\Maxi\\Documents\\UNSA\\LAS\\5to Año\\1er cuatrimestre\\Optativa (Opt. Conc. y Paralela)\\Unidad 2\\TP3\\ACOSCP\\instances\\'
        resultsDir='C:\\Users\\Maxi\\Documents\\UNSA\\LAS\\5to Año\\1er cuatrimestre\\Optativa (Opt. Conc. y Paralela)\\Unidad 2\\TP3\\ACOSCP\\results\\'

        fileName = 'scp41.sol'

        alpha = 1
        beta = 2
        rho = 0.1
        Q0 = 0.7
        iters = 2
        ants = 10
        initialValue = 0.001

        objACOSCP = ACOSCP.clsACOSCP()

        objACOSCP.setAlpha(alpha)
        objACOSCP.setBeta(beta)
        objACOSCP.setRho(rho)
        objACOSCP.setQ0(Q0)
        objACOSCP.setInitialValue(initialValue)

        objACOSCP.setNbrOfIters(iters)
        objACOSCP.setNbrOfAnts(ants)
        
        objACOSCP.setInstanceDir(instanceDir)
        objACOSCP.setResultDir(resultsDir)
        objACOSCP.setInstanceName(instanceName)

        objACOSCP.openFile()

        objACOSCP.solveProblem()
        print ("\n\nTERMINO!")



                
                
