#ifndef __TFLM_ZSP_PREPARE_STRIDESLICE_S8_H__
#define __TFLM_ZSP_PREPARE_STRIDESLICE_S8_H__
#include "tflm_zsp_prepare_common.h"

typedef struct{
    int32_t start0;
    int32_t start1;
    int32_t start2;
    int32_t start3;
    int32_t start4;
    int32_t stop0;
    int32_t stop1;
    int32_t stop2;
    int32_t stop3;
    int32_t stop4;
    int32_t strides0;
    int32_t strides1;
    int32_t strides2;
    int32_t strides3;
    int32_t strides4;
    int32_t input_shape0;
    int32_t input_shape1;
    int32_t input_shape2;
    int32_t input_shape3;
    int32_t input_shape4;
}OpDataStridedSlice;
/**
 *    Parameters:
 *        op_context_begin                    :    Fetch from (node_>inputs->data[kStridedSliceBeginTensor]);
 *        op_context_end                        :    Fetch from (node_>inputs->data[kStridedSliceEndTensor]);
 *        op_context_strides                    :    Fetch from (node_>inputs->data[kStridedSliceStridesTensor]);
 *        op_context_params_begin_mask        :    Fetch from params = (node->builtin_data), params->begin_mask
 *        op_context_params_end_mask            :    Fetch from params = (node->builtin_data), params->end_mask
 *        op_context_params_shrink_axis_mask    :    Fetch from params = (node->builtin_data), params->shrink_axis_mask
 *
 * **/


TfLiteStatus tflm_zsp_prepare_stridedslice_s8(int32_t* op_context_begin,
                                                int32_t* op_context_end,
                                                int32_t* op_context_strides,
                                                int32_t op_context_params_begin_mask,
                                                int32_t op_context_params_end_mask,
                                                int32_t op_context_params_shrink_axis_mask,
                                                int32_t input_dims_size,
                                                int32_t *input_dims_data,
                                                OpDataStridedSlice *data
                                                );

#endif
