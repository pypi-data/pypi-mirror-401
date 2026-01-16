#ifndef __ZSP_HAL_CV_DUMP_H__
#define __ZSP_HAL_CV_DUMP_H__

//#include "zsp_nn_api.h"

typedef enum {
	PARATYPE_POINTER=0x20000,
//====================
	PARATYPE_UINT8,
	PARATYPE_UINT16,
    PARATYPE_UINT32,
    PARATYPE_UINT64,
	PARATYPE_INT8,
    PARATYPE_INT16,
    PARATYPE_INT32,
    PARATYPE_INT64,
    PARATYPE_FLOAT,
    PARATYPE_DOUBLE,
    PARATYPE_SIZE_T,
//====================
    PARATYPE_STRUCT_CONTEXT,
    PARATYPE_STRUCT_ACTIVATION,
    PARATYPE_STRUCT_DIMS,
    PARATYPE_STRUCT_PER_TENSOR_QUANT_PARAMS,
    PARATYPE_STRUCT_PER_CHANNEL_QUANT_PARAMS,
    PARATYPE_STRUCT_FC_PARAMS,
//====================
    PARATYPE_STRUCT_POOL_PARAMS,
//====================
    PARATYPE_STRUCT_SVDF_PARAMS,
//===================
    PARATYPE_STRUCT_CONV_PARAMS,
//==================
    PARATYPE_STRUCT_DEPTHWISE_CONV_PARAMS


} para_type_e;

typedef struct
{
	char* name;
	para_type_e type;
	const void *value;
    int size; //only for PARATYPE_POINTER
} dump_para_t;

typedef struct
{
    int32_t *multiplier; /**< Multiplier values */
    int32_t *shift;      /**< Shift values */
    int multiplier_size;
    int shift_size;
}zsp_nn_per_channel_quant_params_dump;



void zsp_nn_dump_parameters(dump_para_t* dump_para_p, int para_nums, char *kernel_name, char* in_or_out, char *mask);


#endif
