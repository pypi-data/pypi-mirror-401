#ifndef __TFLM_ZSP_PREPROCESS_DEPTHWISE_CONVOLVE_H__
#define __TFLM_ZSP_PREPROCESS_DEPTHWISE_CONVOLVE_H__
#include <stdint.h>


/********************************************
*
*
*	filter_src: src filter data
*	filter_dst: Point to the transposed filter data
*		size = (((filter_dims_w+3)>>2)<<2) *filter_dims_h * input_dims_c * depth_multiplier * sizeof(int8_t)  (byte)
*
**********************************************/

void tflm_zsp_filter_trans_int8_depthwise_convolve(
                        int8_t* filter_src,
                        int8_t* filter_dst,
                        int32_t filter_dims_n,
                        int32_t filter_dims_w,
                        int32_t filter_dims_h,
                        int32_t input_dims_c,
                        int32_t depth_multiplier);

/**********************************************
*preprocess_buf:
*       size = input_dims_c * depth_multiplier * (sizeof(int64_t) + sizeof(int32_t))
*
***********************************************/

void tflm_zsp_preprocess_depthwise_convolve(
      int8_t* preprocess_buf,
      int32_t* bias_data,
      int32_t* output_multiplier,
      int32_t* output_shift,
      int8_t*  filter_data,
      int32_t filter_dims_n,
      int32_t filter_dims_h,
      int32_t filter_dims_w,
      int32_t input_dims_c,
      int32_t depth_multiplier,
      int32_t input_offset,
      int32_t output_offset,
      int32_t quantized_activation_min,
      int32_t quantized_activation_max);


#endif
