#ifndef TFLM_ZSP_PREPARE_SPLIT_H__
#define TFLM_ZSP_PREPARE_SPLIT_H__
#include "tflm_zsp_prepare_common.h"

typedef struct{
    int32_t output_count;
    int32_t outer_size;
    int32_t copy_size0;
    int32_t copy_size1;
    int32_t copy_size2;
    int32_t copy_size3;
    int32_t copy_size4;
}OpDataSplit;

/**
 * Parameters:
 *             split_axis:             : node->inputs[kSplitvAxisTensor].
 *            output0_dims_axis_data: The axis_value dimension of first output tensor
 *
 *    Details:
 *        axis_value = (split_axis > 0)? split_axis: split_axis + input_dims_size;
 *
 * **/
TfLiteStatus tflm_zsp_prepare_split(int32_t split_axis,
                                int32_t node_num_outputs,
                                int32_t input_type,
                                int32_t input_dims_size,
                                int32_t *input_dims_data,
                                int32_t output0_dims_axis_data,
                                OpDataSplit *data
                                );

#endif
