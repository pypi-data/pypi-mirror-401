#include "tflm_zsp_preprocess_common.h"
#include "tflm_zsp_preprocess_depthwise_conv_s8.h"
#include <string.h>
#include <stdlib.h>

#ifdef ZSP_NN_DUMP
#include "zsp_nn_dump.h"
#endif

void tflm_zsp_filter_trans_int8_depthwise_convolve(
                        int8_t* filter_src,
                        int8_t* filter_dst,
                        int32_t filter_dims_n,
                        int32_t filter_dims_w,
                        int32_t filter_dims_h,
                        int32_t input_dims_c,
                        int32_t depth_multiplier)

{


#ifdef ZSP_NN_DUMP

  dump_para_t TFLM_DEPTHWISE_CONVOLVE_FILTER_TRANS_PARAMS_LIST_NAMES[7] =
  {
        {"filter_src", PARATYPE_POINTER, filter_src,
         filter_dims_h * filter_dims_w * input_dims_c},
         {"filter_dst", PARATYPE_POINTER, filter_dst,
          (((filter_dims_w + 3) >> 2) << 2) * filter_dims_h * input_dims_c *
              sizeof(int8_t)},
         {"filter_dims_n", PARATYPE_INT32, &filter_dims_n},
         {"filter_dims_w", PARATYPE_INT32, &filter_dims_w},
         {"filter_dims_h", PARATYPE_INT32, &filter_dims_h},
         {"input_dims_c", PARATYPE_INT32, &input_dims_c},
         {"depth_multiplier", PARATYPE_INT32, &depth_multiplier}
   };

  char mask[9] = {1,0, 1, 1, 1, 1, 1};
  zsp_nn_dump_parameters(TFLM_DEPTHWISE_CONVOLVE_FILTER_TRANS_PARAMS_LIST_NAMES,7, "depthwise_convolve_filter_trans_s8", "in", mask);

#endif

    int32_t h, ich, n;
    int32_t nblock_w = ((filter_dims_w + 3) >> 2) << 2;
    int8_t* in_ptr1, * in_ptr2;
    int8_t* out_ptr1, * out_ptr2;
	int32_t filter_dims_c = input_dims_c * depth_multiplier;
    int8_t* filter_nchw = (int8_t *)malloc(filter_dims_n * filter_dims_w * filter_dims_h * filter_dims_c);

    tflm_zsp_convert_nhwc_to_nchw(filter_src, filter_nchw, filter_dims_n,
                                filter_dims_h, filter_dims_w, filter_dims_c);

    for (ich = 0; ich < input_dims_c; ich++)
    {
      in_ptr1 = filter_nchw + ich * filter_dims_w * filter_dims_h * depth_multiplier;
        out_ptr1 = filter_dst + ich * nblock_w * filter_dims_h * depth_multiplier;
        for (n = 0; n < depth_multiplier; n++)
        {
            in_ptr2 = in_ptr1 + n * filter_dims_w * filter_dims_h;
            out_ptr2 = out_ptr1 + n * nblock_w * filter_dims_h;
            for (h = 0; h < filter_dims_h; h++)
            {
                memset(out_ptr2, 0, nblock_w * sizeof(int8_t));
                memcpy(out_ptr2, in_ptr2, filter_dims_w * sizeof(int8_t));
                out_ptr2 += nblock_w;
                in_ptr2 += filter_dims_w;
            }
        }
    }

    free(filter_nchw);

#ifdef ZSP_NN_DUMP

    char mask_out[7] = {0, 1, 0, 0, 0, 0, 0};
    zsp_nn_dump_parameters(
        TFLM_DEPTHWISE_CONVOLVE_FILTER_TRANS_PARAMS_LIST_NAMES, 7,
        "depthwise_convolve_filter_trans_s8", "out", mask_out);
#endif

}



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
	  int32_t quantized_activation_max){


#ifdef ZSP_NN_DUMP
    dump_para_t TFLM_DEPTHWISE_CONVOLVE_PREPROCESS_PARAMS_LIST_NAMES[14] =
      {
            {"preprocess_buf", PARATYPE_POINTER, preprocess_buf,
                depth_multiplier * input_dims_c * (sizeof(int32_t)+sizeof(int64_t))},
            {"bias_data", PARATYPE_POINTER, bias_data,
              (bias_data)?input_dims_c* depth_multiplier * sizeof(int32_t):0},
            {"output_multiplier", PARATYPE_POINTER, output_multiplier,
             input_dims_c * depth_multiplier * sizeof(int32_t)},
            {"output_shift", PARATYPE_POINTER, output_shift,
             input_dims_c * depth_multiplier * sizeof(int32_t)},
            {"filter_data", PARATYPE_POINTER, filter_data,
			filter_dims_n * filter_dims_h * filter_dims_w * input_dims_c * depth_multiplier * sizeof(int8_t)},
            {"filter_dims_n", PARATYPE_INT32, &filter_dims_n},
            {"filter_dims_h", PARATYPE_INT32, &filter_dims_h},
            {"filter_dims_w", PARATYPE_INT32, &filter_dims_w},
            {"input_dims_c", PARATYPE_INT32, &input_dims_c},
            {"depth_multiplier", PARATYPE_INT32, &depth_multiplier},
            {"input_offset", PARATYPE_INT32, &input_offset},
            {"output_offset", PARATYPE_INT32, &output_offset},
            {"quantized_activation_min", PARATYPE_INT32,&quantized_activation_min},
            {"quantized_activation_max", PARATYPE_INT32, &quantized_activation_max},
      };

  char mask[14] = {0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
  zsp_nn_dump_parameters(TFLM_DEPTHWISE_CONVOLVE_PREPROCESS_PARAMS_LIST_NAMES,
                         14, "depthwise_convolve_preprocess_s8", "in", mask);
#endif

    int32_t i_input_ch, i_ch_mult, idx_out_ch, acc;
    int32_t i_ker;
    int32_t filter_dims_c = input_dims_c * depth_multiplier;
    int8_t* filter_nchw = (int8_t *)malloc(filter_dims_n * filter_dims_h * filter_dims_w * filter_dims_c);

    tflm_zsp_convert_nhwc_to_nchw(filter_data, filter_nchw, filter_dims_n,
                                filter_dims_h, filter_dims_w, filter_dims_c);

    memset(preprocess_buf, 0,
        depth_multiplier * input_dims_c * (sizeof(int32_t) + sizeof(int64_t)));

    int64_t* quanter_ptr = (int64_t*)preprocess_buf;
    int32_t* input_offset_ptr = (int32_t*)(preprocess_buf + depth_multiplier * input_dims_c * sizeof(int64_t));

    for (i_input_ch = 0; i_input_ch < input_dims_c; i_input_ch++)
    {
        for (i_ch_mult = 0; i_ch_mult < depth_multiplier; i_ch_mult++)
        {
            idx_out_ch = i_ch_mult + i_input_ch * depth_multiplier;
				
			quanter_ptr[idx_out_ch] = tflm_zsp_requantize_int8((output_multiplier[idx_out_ch]) ,
													quantized_activation_max,
													quantized_activation_min,
													output_offset,
													output_shift[idx_out_ch]);
			
            acc = 0;
            for (i_ker = 0; i_ker < filter_dims_w * filter_dims_h; i_ker++)
            {
                acc += filter_nchw[i_ker + idx_out_ch * filter_dims_w * filter_dims_h];
            }

            acc *= input_offset;
            if (bias_data)
            {
                acc += bias_data[idx_out_ch];
            }
            *input_offset_ptr++ = acc;
        }
    }

    free(filter_nchw);

#ifdef ZSP_NN_DUMP

    char mask_out[14] = {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    zsp_nn_dump_parameters(TFLM_DEPTHWISE_CONVOLVE_PREPROCESS_PARAMS_LIST_NAMES,
                           14, "depthwise_convolve_preprocess_s8", "out",
                           mask_out);

#endif


}
