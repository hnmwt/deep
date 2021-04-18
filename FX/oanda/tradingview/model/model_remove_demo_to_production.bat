 rem モデルをdemoからproductionにコピーする
 
 copy /Y .\USDJPY_15m_turning_high_demo\model.hdf5 .\USDJPY_15m_turning_high_production\model.hdf5
 copy /Y .\USDJPY_15m_turning_high_demo\param.hdf5 .\USDJPY_15m_turning_high_production\param.hdf5
 
 copy /Y .\USDJPY_15m_turning_low_demo\model.hdf5 .\USDJPY_15m_turning_low_production\model.hdf5
 copy /Y .\USDJPY_15m_turning_low_demo\param.hdf5 .\USDJPY_15m_turning_low_production\param.hdf5
 
 copy /Y .\USDJPY_15m_turning_close_demo\model.hdf5 .\USDJPY_15m_turning_close_production\model.hdf5
 copy /Y .\USDJPY_15m_turning_close_demo\param.hdf5 .\USDJPY_15m_turning_close_production\param.hdf5
 
 pause