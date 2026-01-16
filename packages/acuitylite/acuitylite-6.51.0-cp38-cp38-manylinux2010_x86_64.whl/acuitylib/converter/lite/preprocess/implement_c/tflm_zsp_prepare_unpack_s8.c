#include "tflm_zsp_prepare_unpack_s8.h"


TfLiteStatus tflm_zsp_prepare_unpack_s8(TfLiteUnpackParams* params,
                                                int32_t input_data_type,
                                                int32_t *input_dims_data,
                                                int32_t input_dims_size,
                                                OpDataUnpack *data){


    int32_t axis_value = params->axis;
    int32_t outer_size = 1;
    int32_t datatype_bytes = 0;
    int32_t copy_size = 1;
    int32_t i = 0;

    if(axis_value < 0){
        axis_value += input_dims_size;
    }

    outer_size = 1;
    for(i = 0; i< axis_value; i++){
        outer_size *= input_dims_data[i];
    }

    datatype_bytes = tflm_zsp_sizeof_type(input_data_type);
    copy_size = 1 * datatype_bytes;

    for(i = axis_value + 1; i< input_dims_size; i++){
        copy_size *= input_dims_data[i];
    }

    data->num = params->num;
    data->copy_size = copy_size;
    data->outer_size = outer_size;

    return kTfLiteOk;
}

