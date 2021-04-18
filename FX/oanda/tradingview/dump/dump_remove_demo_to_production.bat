 rem モデルをdemoからproductionにコピーする
 
 copy /Y .\USDJPY_15m_dump_turning_high_demo\X_train_scaler.sav .\USDJPY_15m_dump_turning_high_production\X_train_scaler.sav
 copy /Y .\USDJPY_15m_dump_turning_high_demo\y_train_scaler.sav .\USDJPY_15m_dump_turning_high_production\y_train_scaler.sav
 
 copy /Y .\USDJPY_15m_dump_turning_low_demo\X_train_scaler.sav .\USDJPY_15m_dump_turning_low_production\X_train_scaler.sav
 copy /Y .\USDJPY_15m_dump_turning_low_demo\y_train_scaler.sav .\USDJPY_15m_dump_turning_low_production\y_train_scaler.sav
 
 copy /Y .\USDJPY_15m_dump_turning_close_demo\X_train_scaler.sav .\USDJPY_15m_dump_turning_close_production\X_train_scaler.sav
 copy /Y .\USDJPY_15m_dump_turning_close_demo\y_train_scaler.sav .\USDJPY_15m_dump_turning_close_production\y_train_scaler.sav
 
 pause