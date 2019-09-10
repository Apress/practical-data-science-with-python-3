#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fits a linear model using streaming regression.

@author: Ervin Varga
"""
def fit_and_predict(sparkSession, ts):
    import numpy as np
    from sklearn.model_selection import train_test_split
    from pyspark.streaming import StreamingContext
    from pyspark.mllib.regression import StreamingLinearRegressionWithSGD

    def to_scaled_rdd(pandasDataFrame):
        import pandas as pd
        from sklearn.preprocessing import RobustScaler
        from pyspark.mllib.regression import LabeledPoint

        regressors = pandasDataFrame.columns[1:]
        num_regressors = len(regressors)
        # FIX ME: As a bonus exercise, read the last paragraph from section about residual
        # plots and make the necessary bug fix! Compare the behavior of this version with the
        # fixed one and see whether you can decipher anything from the outputs.
        scaler = RobustScaler()
        scaled_regressors = scaler.fit_transform(pandasDataFrame[regressors])
        scaled_pandasDataFrame = pd.DataFrame(scaled_regressors, columns=regressors)
        scaled_pandasDataFrame['target'] = pandasDataFrame[pandasDataFrame.columns[0]].values
        
        sparkDataFrame = sparkSession.createDataFrame(scaled_pandasDataFrame)
        return sparkDataFrame.rdd.map(
                lambda row: LabeledPoint(row[num_regressors], row[:num_regressors]))

    def report_accuracy(result_rdd):
        from pyspark.mllib.evaluation import RegressionMetrics
        
        if not result_rdd.isEmpty():
            metrics = RegressionMetrics(
                    result_rdd.map(lambda t: (float(t[1]), float(t[0]))))
            print("MSE = %s" % metrics.meanSquaredError)
            print("RMSE = %s" % metrics.rootMeanSquaredError)
            print("R-squared = %s" % metrics.r2)
            print("MAE = %s" % metrics.meanAbsoluteError)
            print("Explained variance = %s" % metrics.explainedVariance)        
    
    df_train, df_test = train_test_split(ts, test_size=0.2, shuffle=False)    
    train_rdd = to_scaled_rdd(df_train)
    test_rdd = to_scaled_rdd(df_test)
    
    streamContext = StreamingContext(sparkSession.sparkContext, 1)
    train_stream = streamContext.queueStream([train_rdd])
    test_stream = streamContext.queueStream([test_rdd])
    
    numFeatures = len(ts.columns) - 1
    model = StreamingLinearRegressionWithSGD(stepSize=0.05, numIterations=300)
    np.random.seed(0)
    model.setInitialWeights(np.random.rand(numFeatures))

    model.trainOn(train_stream)
    result_stream = model.predictOnValues(test_stream.map(lambda lp: (lp.label, lp.features)))
    result_stream.cache()
    result_stream.foreachRDD(report_accuracy)

    streamContext.start()
    streamContext.awaitTermination()