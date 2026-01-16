
#ifndef __MODEL_DATA_H__
#define __MODEL_DATA_H__


#ifdef __ZSP__
#define SEC_CONST_DATA __attribute__((section(".data")))
#else
#define SEC_CONST_DATA
#endif



#TFLMZSP_REPLACE_DEFINE_CONST_DATA#


#endif