#include "tflm_zsp_preprocess_common.h"
#include "tflm_zsp_preprocess_convolve.h"
#include <string.h>
#include <stdlib.h>

#ifdef ZSP_NN_DUMP
#include "zsp_nn_dump.h"
#endif

void tflm_zsp_filter_trans_int8_convolve(int8_t *filter_src,
										int8_t * filter_dst,
										int32_t input_dims_c,
										int32_t output_dim_c,
										int32_t filter_dims_h,
										int32_t filter_dims_w,
										int32_t filter_dims_c){


#ifdef ZSP_NN_DUMP
  int32_t reorder_filter_buf_size = 0;

  dump_para_t TFLM_CONVOLVE_FILTER_TRANS_PARAMS_LIST_NAMES[7] = {
      {"filter_src", PARATYPE_POINTER, filter_src,
       output_dim_c * filter_dims_h * filter_dims_w * filter_dims_c},
      {"filter_dst", PARATYPE_POINTER, filter_dst,
       reorder_filter_buf_size},
      {"input_dims_c", PARATYPE_INT32, &input_dims_c},
      {"output_dim_c", PARATYPE_INT32, &output_dim_c},
      {"filter_dims_h", PARATYPE_INT32, &filter_dims_h},
      {"filter_dims_w", PARATYPE_INT32, &filter_dims_w},
      {"filter_dims_c", PARATYPE_INT32, &filter_dims_c}
  };
  char mask[7] = {1,0,1,1,1,1,1};
  zsp_nn_dump_parameters(TFLM_CONVOLVE_FILTER_TRANS_PARAMS_LIST_NAMES, 7,
                         "convolve_filter_trans_s8", "in", mask);
#endif

	int8_t* src =  filter_src;
	int8_t* dst = 0;
	int32_t size;
    int32_t groups = input_dims_c / filter_dims_c;
    int32_t output_ch_per_group = output_dim_c / groups;

    int32_t output_ch_per_group_align = (output_ch_per_group + 3) >> 2 << 2;
    int32_t ksize_align = (filter_dims_c * filter_dims_h * filter_dims_w + 7) >> 3 << 3;
  	int8_t *filter_nchw = (int8_t *)malloc(output_dim_c *filter_dims_h* filter_dims_w* filter_dims_c);

    int8_t* dst_ptr1;
    int8_t* src_ptr1;
    int8_t* dst_ptr2;
    int8_t* src_ptr2;

    tflm_zsp_convert_nhwc_to_nchw(filter_src, filter_nchw, output_dim_c,
                                filter_dims_h, filter_dims_w, filter_dims_c);

	src = filter_nchw;
	dst = filter_dst;
    size = ksize_align * output_ch_per_group_align * groups;
    memset(dst, 0, size);

    for (int32_t i_group = 0; i_group < groups; i_group++) {
        dst_ptr1 = dst;
        src_ptr1 = src;
        src_ptr2 = src_ptr1;
        for (int32_t i_out_ch = 0; i_out_ch < output_ch_per_group; i_out_ch++) {
            if (i_out_ch % 4 == 0) {

                dst_ptr1 = dst + i_out_ch * ksize_align;
            }

            dst_ptr2 = dst_ptr1;

            for (int32_t i_cnt = 0; i_cnt < (filter_dims_h * filter_dims_w * filter_dims_c) / 4; i_cnt++) {
                dst_ptr2[0] = *src_ptr2++;
                dst_ptr2[1] = *src_ptr2++;
                dst_ptr2[2] = *src_ptr2++;
                dst_ptr2[3] = *src_ptr2++;
                dst_ptr2 += 16;
            }
            for (int32_t i_cnt = 0; i_cnt < ((filter_dims_h * filter_dims_w * filter_dims_c) & 0x3); i_cnt++) {
                dst_ptr2[i_cnt] = *src_ptr2++;
                ;
            }
            dst_ptr1 += 4;
        }
        dst += ksize_align * output_ch_per_group_align;
        src += filter_dims_c * filter_dims_h * filter_dims_w * output_ch_per_group;
    }

    free(filter_nchw);

#ifdef ZSP_NN_DUMP

    char mask_out[7] = {0, 1, 0, 0, 0, 0, 0};


    reorder_filter_buf_size = ksize_align *
                                     output_ch_per_group_align * groups;

    zsp_nn_dump_parameters(TFLM_CONVOLVE_FILTER_TRANS_PARAMS_LIST_NAMES, 7,
                           "convolve_filter_trans_s8", "out", mask_out);
#endif


}



void tflm_zsp_preprocess_int8_convolve(
    int8_t* preprocess_buf, int8_t* reorder_filter_buf, int32_t* output_multiplier,
    int32_t* output_shift, int32_t* bias_data, int32_t out_activation_min,
    int32_t out_activation_max, int32_t out_offset, int32_t output_dims_c,
    int32_t filter_dims_c, int32_t filter_dims_h, int32_t filter_dims_w,
    int32_t input_offset) {


#ifdef ZSP_NN_DUMP

      dump_para_t TFLM_CONVOLVE_PREPROCESS_PARAMS_LIST_NAMES[12] = {
          {"preprocess_buf", PARATYPE_POINTER, preprocess_buf,
           (((output_dims_c + 3) >> 2) << 2) * sizeof(int32_t) +
               (((output_dims_c + 3) >> 2) << 2) * sizeof(int64_t)},
          {"output_multiplier", PARATYPE_POINTER, output_multiplier,
           output_dims_c * sizeof(int32_t)},
          {"output_shift", PARATYPE_POINTER, output_shift,
           output_dims_c * sizeof(int32_t)},
          {"bias_data", PARATYPE_INT32, bias_data,
           (bias_data)?output_dims_c * sizeof(int32_t):0},
          {"filter_dims_w", PARATYPE_INT32, &filter_dims_w},
          {"filter_dims_c", PARATYPE_INT32, &filter_dims_c},
          {"filter_dims_w", PARATYPE_INT32, &filter_dims_w},
          {"filter_dims_c", PARATYPE_INT32, &filter_dims_c},
          {"filter_dims_w", PARATYPE_INT32, &filter_dims_w},
          {"filter_dims_c", PARATYPE_INT32, &filter_dims_c},
          {"filter_dims_w", PARATYPE_INT32, &filter_dims_w},
          {"filter_dims_c", PARATYPE_INT32, &filter_dims_c}
      };

    char mask[12] = {0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
    zsp_nn_dump_parameters(TFLM_CONVOLVE_PREPROCESS_PARAMS_LIST_NAMES, 12,
                         "convolve_preprocess_s8", "in",  mask);
#endif

  memset(preprocess_buf, 0, (((output_dims_c + 3) >> 2) << 2) * sizeof(int32_t) + (((output_dims_c + 3) >> 2) << 2) * sizeof(int64_t));

  int64_t* quant_param = (int64_t*)preprocess_buf;
  uint64_t temp64;
  uint64_t scale;
  uint64_t lshft;
  uint64_t rshft;
  uint64_t quanter;
  int32_t i, j;
  int32_t shift;
  int32_t quant_param_size =
      (((output_dims_c + 3) >> 2) << 2) * sizeof(int64_t);
  int32_t* filter_sum = (int32_t*)((int8_t*)preprocess_buf + quant_param_size);

  int32_t sum_out_ch0, sum_out_ch1, sum_out_ch2, sum_out_ch3;
  const int8_t* filter_data_ptr = 0;
  const int8_t* filter_data_ptr1 = 0;
  int32_t inner_lpcnt =
      (filter_dims_h * filter_dims_w * filter_dims_c + 3) >> 2;
  //int32_t kc_align = (filter_dims_c + 7) >> 3 << 3;
  int32_t ksize_align = (filter_dims_h * filter_dims_w * filter_dims_c + 7) >> 3 << 3;
  int32_t outter_lpcnt0 = (output_dims_c) >> 2;
  int32_t outter_lpcnt1 = output_dims_c & 0x3;

  temp64 = ((uint64_t)out_activation_min & 0xff) << 16;
  temp64 |= ((uint64_t)out_activation_max & 0xff) << 24;
  temp64 |= ((uint64_t)out_offset & 0xff) << 32;

  for (i = 0; i < output_dims_c; i++) {
    scale = (uint64_t)((output_multiplier[i] >> 16) & 0xffff);
    shift = output_shift[i];
    shift = shift + 1;
    lshft = shift > 0 ? ((uint64_t)(shift & 0x7) << 40) : (0);
    rshft = shift > 0 ? (0) : ((uint64_t)(-shift & 0x1f) << 43);

    quanter = temp64 | scale | rshft | lshft;
    quant_param[i] = quanter;
  }

  for (j = 0; j < outter_lpcnt0; j++) {
    filter_data_ptr = reorder_filter_buf;
    sum_out_ch0 = 0;
    sum_out_ch1 = 0;
    sum_out_ch2 = 0;
    sum_out_ch3 = 0;

    for (i = 0; i < inner_lpcnt; i++) {
      sum_out_ch0 += (*filter_data_ptr++);
      sum_out_ch0 += (*filter_data_ptr++);
      sum_out_ch0 += (*filter_data_ptr++);
      sum_out_ch0 += (*filter_data_ptr++);

      sum_out_ch1 += (*filter_data_ptr++);
      sum_out_ch1 += (*filter_data_ptr++);
      sum_out_ch1 += (*filter_data_ptr++);
      sum_out_ch1 += (*filter_data_ptr++);

      sum_out_ch2 += (*filter_data_ptr++);
      sum_out_ch2 += (*filter_data_ptr++);
      sum_out_ch2 += (*filter_data_ptr++);
      sum_out_ch2 += (*filter_data_ptr++);

      sum_out_ch3 += (*filter_data_ptr++);
      sum_out_ch3 += (*filter_data_ptr++);
      sum_out_ch3 += (*filter_data_ptr++);
      sum_out_ch3 += (*filter_data_ptr++);
    }

    sum_out_ch0 = input_offset * sum_out_ch0;
    sum_out_ch1 = input_offset * sum_out_ch1;
    sum_out_ch2 = input_offset * sum_out_ch2;
    sum_out_ch3 = input_offset * sum_out_ch3;

    if (bias_data) {
      sum_out_ch0 += bias_data[4 * j + 0];
      sum_out_ch1 += bias_data[4 * j + 1];
      sum_out_ch2 += bias_data[4 * j + 2];
      sum_out_ch3 += bias_data[4 * j + 3];
    }

    filter_sum[4 * j + 0] = sum_out_ch0;
    filter_sum[4 * j + 1] = sum_out_ch1;
    filter_sum[4 * j + 2] = sum_out_ch2;
    filter_sum[4 * j + 3] = sum_out_ch3;

    reorder_filter_buf = reorder_filter_buf + 4 * ksize_align;

  }

  filter_data_ptr = reorder_filter_buf;
  for (j = 0; j < outter_lpcnt1; j++) {
    filter_data_ptr1 = filter_data_ptr;
    sum_out_ch0 = 0;
    for (i = 0; i < inner_lpcnt; i++) {
      sum_out_ch0 += (*filter_data_ptr1++);
      sum_out_ch0 += (*filter_data_ptr1++);
      sum_out_ch0 += (*filter_data_ptr1++);
      sum_out_ch0 += (*filter_data_ptr1++);
      filter_data_ptr1 += 12;
    }

    sum_out_ch0 = input_offset * sum_out_ch0;

    if (bias_data) {
      sum_out_ch0 += bias_data[4 * outter_lpcnt0 + j];
    }

    filter_data_ptr += 4;  // next filter
    filter_sum[4 * outter_lpcnt0 + j] = sum_out_ch0;
  }

#ifdef ZSP_NN_DUMP

  char mask_out[12] = {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
  zsp_nn_dump_parameters(TFLM_CONVOLVE_PREPROCESS_PARAMS_LIST_NAMES, 12,
                         "convolve_preprocess_s8", "out", mask_out);
#endif
}

void tflm_zsp_filter_trans_int8_convolve_small_width(int8_t *filter_src,
										int8_t * filter_dst,
										int32_t output_dim_c,
										int32_t filter_dims_h,
										int32_t filter_dims_w,
										int32_t filter_dims_c){

	int32_t remind_kernel_c_align16 = (((filter_dims_c + 15)>>4)<<4) - filter_dims_c;

	for(int i = 0; i < filter_dims_h; i++){
		for(int j = 0; j < filter_dims_w; j++){
			/////////
			for(int k = 0; k < filter_dims_c; k++){
				for(int l = 0; l < output_dim_c; l++){
					*filter_dst++ = *(filter_src + filter_dims_h * filter_dims_w * filter_dims_c * l);
				}
				filter_src++;
			}
			////////
			for(int k = 0; k < remind_kernel_c_align16; k++){
				for(int l = 0; l < output_dim_c; l++){
					*filter_dst++ = 0;
				}
			}
		}
	}
}

void tflm_zsp_preprocess_int8_convolve_small_width(
	    int8_t* preprocess_buf, int8_t* filter_src, int32_t* output_multiplier,
	    int32_t* output_shift, int32_t* bias_data, int32_t out_activation_min,
	    int32_t out_activation_max, int32_t out_offset, int32_t output_dims_c,
	    int32_t filter_dims_c, int32_t filter_dims_h, int32_t filter_dims_w,
	    int32_t input_dims_c, int32_t input_offset){

	int32_t reorder_filter_size = 0;
    int32_t groups = input_dims_c / filter_dims_c;
    int32_t output_ch_per_group = output_dims_c / groups;

    int32_t output_ch_per_group_align = (output_ch_per_group + 3) >> 2 << 2;
    int32_t ksize_align = (filter_dims_c * filter_dims_h * filter_dims_w + 7) >> 3 << 3;

    //int32_t size;
    reorder_filter_size = ksize_align * output_ch_per_group_align * groups;
    
    int8_t* reorder_filter_buf = malloc(reorder_filter_size);

	int8_t *filter_dst = malloc(reorder_filter_size);

	tflm_zsp_filter_trans_int8_convolve(filter_src,
											reorder_filter_buf,
											filter_dims_c,
											output_dims_c,
											filter_dims_h,
											filter_dims_w,
											filter_dims_c);



    tflm_zsp_preprocess_int8_convolve(
    		preprocess_buf, reorder_filter_buf, output_multiplier,
    		output_shift, (int32_t *)bias_data, out_activation_min,
    		out_activation_max, out_offset, output_dims_c,
    		filter_dims_c, filter_dims_h, filter_dims_w,
    		input_offset);

	if(filter_dst)
		free(filter_dst);
}
