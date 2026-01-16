#ifndef __TFLM_ZSP_PREPROCESS_CONVOLVE_H__
#define __TFLM_ZSP_PREPROCESS_CONVOLVE_H__
#include <stdint.h>

/******************************************
*	filter_src: 				point to filter data
*
*	filter_dst:					point to the final converted data
*
*								int32_t groups = input_dims_c / filter_dims_c;
*								int32_t output_ch_per_group = output_dim_c / groups;
*								int32_t output_ch_per_group_align = (output_ch_per_group + 3) >> 2 << 2;
*								int32_t ksize_align = (filter_dims_c *  filter_dims_h * filter_dims_w  + 7) >> 3 << 3;
*
*								int32_t size =  ksize_align * output_ch_per_group_align * groups; (byte)
*
*
******************************************/

void tflm_zsp_filter_trans_int8_convolve(int8_t *filter_src,
										int8_t * filter_dst,
										int32_t input_dims_c,
										int32_t output_dim_c,
										int32_t filter_dims_h,
										int32_t filter_dims_w,
										int32_t filter_dims_c);

/************************************************************
*	preprocess_buf: 			point to the preprocessed data
*								size = (((output_dims_c + 3) >> 2)<<2) * sizeof(int32_t) +
*									(((output_dims_c + 3) >> 2)<<2) * sizeof(int64_t) (byte)
*
*	reorder_filter_buf:			point to the filter data that is reordered by function tflm_zsp_filter_trans_int8_convolve
*
*
***********************************************************/


void tflm_zsp_preprocess_int8_convolve(int8_t* preprocess_buf,
										 int8_t * reorder_filter_buf,
										 int32_t* output_multiplier,
										 int32_t* output_shift,
										 int32_t* bias_data,
										 int32_t out_activation_min,
										 int32_t out_activation_max,
										 int32_t out_offset,
										 int32_t output_dims_c,
										 int32_t filter_dims_c,
										 int32_t filter_dims_h,
										 int32_t filter_dims_w,
										 int32_t input_offset);
										 
/******************************************
*	Called if conv2d's output_dims.w <= 32 && filter_dims_h != 10 && filter_dims_w != 4 && filter_dims_c >= 16
*	Called if pointwiseconv2d's output_dims.w * output_dims.h <= 32 &&  filter_dims_c >= 16
*		
*
*
*	filter_src: 				point to origin filter data
*
*	filter_dst:					point to the final converted data
*
*
*								size =	(((filter_dims_c + 15)>>4)<<4) * filter_dims_h * filter_dims_w * output_dim_c
******************************************/

void tflm_zsp_filter_trans_int8_convolve_small_width(int8_t *filter_src,
										int8_t * filter_dst,
										int32_t output_dim_c,
										int32_t filter_dims_h,
										int32_t filter_dims_w,
										int32_t filter_dims_c);

/************************************************************
*	Called if conv2d's output_dims.w <= 32 && filter_dims_h != 10 && filter_dims_w != 4 && filter_dims_c >= 16
*	Called if pointwiseconv2d's output_dims.w * output_dims.h <= 32 &&  filter_dims_c >= 16
*
*	preprocess_buf: 			point to the preprocessed data
*								size = (((output_dims_c + 3) >> 2)<<2) * sizeof(int32_t) +
*									(((output_dims_c + 3) >> 2)<<2) * sizeof(int64_t) (byte)
*
*	filter_src:					point to the origin filter data
*
*
***********************************************************/

void tflm_zsp_preprocess_int8_convolve_small_width(
										int8_t* preprocess_buf, 
										int8_t* filter_src, 
										int32_t* output_multiplier,
										int32_t* output_shift, 
										int32_t* bias_data, 
										int32_t out_activation_min,
										int32_t out_activation_max, 
										int32_t out_offset, 
										int32_t output_dims_c,
										int32_t filter_dims_c, 
										int32_t filter_dims_h, 
										int32_t filter_dims_w,
										int32_t input_dims_c, 
										int32_t input_offset);
#endif
