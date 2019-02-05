import pandas as pd
import numpy as np
import datetime
import sys

chunkMapDF = pd.read_csv('data/chunkMap.csv')
QRs = pd.read_csv('QR_Values.csv').set_index('label')



def getSeriesDF(cid, fileName):
    localDF = pd.read_csv('data/Chunks/'+fileName+".csv").drop(columns=['Unnamed: 0'])
    localDF = localDF.loc[localDF['ContestId']==cid]
    localDF = localDF.assign(InvertedTime = localDF['SecondsRemaining'].max()-localDF['SecondsRemaining'])
    localDF = localDF.assign(SummedEntries = localDF['Entries'][::-1].cumsum()[::-1])
    return localDF
def setupSeries(df):
    localDF = df.copy(deep=True)
    localDF = localDF.assign(X=localDF["InvertedTime"]).assign(Y=localDF["SummedEntries"])
    localDF = localDF[['X', 'Y']].sort_values(by=['X'])
    return localDF
def defaultParameters(df):
    random_state = np.random.RandomState(0)
    F = np.eye(2) #Transition Matrix (Identity Matrix)

    Z = list(df['Y']) #Observation matrix
    X0 = [[4.], [.0023]] #Inital parameters guess (?) <<<< NEED VALUES
    P0 = (np.eye(2) + random_state.randn(2, 2)*.1)*100*np.eye(2) #Covariance Matrix (The confidence in our prediction)
    R = random_state.rand()*5.05
#     Q = getQ(random_state)*1000
    Q = [[np.power(9.,62),0.],[0.,np.power(6.,65)]]
    w = np.random.multivariate_normal([0., 0.], Q)
    return {'random_state':random_state, 'F':F, 'Z':Z, 'X0':X0, 'P0':P0, 'R':R, 'Q':Q, 'w':w}
def kalmanFilter(series, parameters, extended=True):
    Xs = []
    
    Pk = parameters['P0'] 
    Xk = parameters['X0'] 
    for n in range(0, len(series)):
        actual = np.array(series.iloc[n]['Y']) #Current actual
        time = np.array(series.iloc[n]['X']) #Current time
        Pk = Pk + parameters["Q"]
                
        Hk, Zk = 0, 0
        if(extended):
            part1 = np.exp(Xk[1][0]*time)
            Hk = [part1, part1*(Xk[0][0]*time)]
            Zk = Xk[0][0]*np.exp(Xk[1][0]*time)
        else:
            Hk = [1., time]
            Zk = np.dot(Hk, Xk) + np.random.normal(loc=0., scale=parameters['R']) #<----- Consider putting Vk instead of R        
        
        Yk = actual - Zk # residuals
        transposedH = [[Hk[0]],[Hk[1]]]
        Sk = np.dot(np.dot(Hk, Pk), transposedH)[0]+parameters['R']
        Kk = np.dot(Pk, transposedH)*(1/Sk)
        Xnext = Xk + Kk*Yk        
        p_part = (np.eye(2)-np.outer(Kk, Hk))
        Pnext = np.dot(p_part, Pk)
        
        Xs.append([Xk[0][0], Xk[1][0]])
        #Set new vars based on current observation
        Pk = Pnext
        Xk = Xnext
    return Xs

def timeString():
    now = datetime.datetime.now()
    return str(now.year) + "-" + str(now.month) + "-" + str(now.day) + "-" + str(now.hour) + "-" + str(now.minute)


if(len(sys.argv)<2):
	print("Please provide qr reference.")
	sys.exit()

qrValName = sys.argv[1]
QR_Vals = QRs.loc[qrValName]




QR_Vals = QRs.loc[qrValName]
for i in range(1, 49)[:]:
    chunkname = 'chunk'+str(i)
    contestIds = chunkMapDF[chunkMapDF['Chunk'] == chunkname]['ContestId']
    
    results = []
    for cid in contestIds[:]:
        df = getSeriesDF(cid, chunkname)
        df = df[df['SecondsRemaining']>240]
        df = setupSeries(df)
        if(len(df)> 10):
            parameters = defaultParameters(df)
            parameters['Q'] = [[QR_Vals['Q1'], 0.0], [0.0, QR_Vals['Q2']]]
            parameters['R'] = QR_Vals['R']


            Xf = kalmanFilter(df, parameters)[-1:][0]
            results.append({'label':qrValName, 'ContestId': cid, 'Xf': Xf})
    pd.DataFrame(results).to_csv('data/'+'results_'+chunkname+"_"+qrValName+"_"+timeString()+".csv")








