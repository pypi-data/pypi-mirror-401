#include "tflm_zsp_preprocess_fully_connected.h"
#include <string.h>

#ifdef ZSP_NN_DUMP
#include "zsp_nn_dump.h"
#endif


void tflm_zsp_filter_trans_int8_fullconnected(int8_t *data_src, int8_t* data_dst, int32_t row_num, int32_t col_num){

#ifdef ZSP_NN_DUMP
  	dump_para_t TFLM_FULLY_CONNECTED_FILTER_TRANS_PARAMS_LIST_NAMES[4] =
	{
		{"data_src", PARATYPE_POINTER, data_src, row_num * col_num},
        {"data_dst", PARATYPE_POINTER, data_dst, row_num * col_num},
        {"output_ch", PARATYPE_INT32, &(row_num)},
        {"filter_n", PARATYPE_INT32,  &(col_num)},
    };

  char mask[4] = {1, 0, 1, 1};
  zsp_nn_dump_parameters(TFLM_FULLY_CONNECTED_FILTER_TRANS_PARAMS_LIST_NAMES, 4, "fully_connected_trans_s8", "in", mask);

#endif
  	tflm_zsp_filter_data pSrc, pDst;
  	pSrc.pData = data_src;
  	pSrc.numRows = row_num;
  	pSrc.numCols = col_num;
  	pDst.pData = data_dst;
  	pDst.numRows = col_num;
  	pDst.numCols = row_num;

	tflm_zsp_mat_trans_int8(&pSrc,&pDst);

#ifdef ZSP_NN_DUMP

        char mask_out[4] = {0, 1, 0, 0};
        zsp_nn_dump_parameters(
            TFLM_FULLY_CONNECTED_FILTER_TRANS_PARAMS_LIST_NAMES, 4, "fully_connected_trans_s8", "out", mask_out);

#endif


}


void tflm_zsp_preprocess_fullconnected(int32_t *data_output, const int32_t *data_bias,
			const int8_t *data_filter ,int32_t filter_offset,
			int32_t input_offset,
			int32_t filter_dim_n, int32_t output_dim_c,
			int32_t output_multiplier,	int32_t quantized_activation_max,
			int32_t quantized_activation_min, int32_t output_offset,
			int32_t output_shift)
{
	int i, j;
#ifdef ZSP_NN_DUMP

		dump_para_t TFLM_FULLY_CONNECTED_PREPROCESS_PARAMS_LIST_NAMES[12] =
		{
				{"data_output", PARATYPE_POINTER, data_output, sizeof(int64_t) + output_dim_c * sizeof(int32_t)},
				{"data_bias", PARATYPE_POINTER, data_bias,
	             (data_bias)?output_dim_c * sizeof(int32_t):0},
				{"data_filter", PARATYPE_POINTER, data_filter, filter_dim_n * output_dim_c},
				{"filter_offset", PARATYPE_INT32, &filter_offset},
				{"input_offset", PARATYPE_INT32, &input_offset},
				{"filter_dim_n", PARATYPE_INT32, &filter_dim_n},
				{"output_dim_c", PARATYPE_INT32, &output_dim_c},
				{"output_multiplier", PARATYPE_INT32, &output_multiplier},
				{"quantized_activation_max", PARATYPE_INT32, &quantized_activation_max},
				{"quantized_activation_min", PARATYPE_INT32, &quantized_activation_min},
				{"output_offset", PARATYPE_INT32, &output_offset},
				{"output_shift", PARATYPE_INT32, &output_shift},
		};

        char mask[12] = {0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
        zsp_nn_dump_parameters(
            TFLM_FULLY_CONNECTED_PREPROCESS_PARAMS_LIST_NAMES, 12, "fully_connected_preprocess_s8", "in", mask);
#endif


	memset(data_output, 0, sizeof(int64_t) + output_dim_c * sizeof(int32_t));

	int32_t total_offset = filter_offset *input_offset* filter_dim_n;

	*(int64_t *)data_output = tflm_zsp_requantize_int8(output_multiplier,
			quantized_activation_max,
			quantized_activation_min,
			output_offset,
			output_shift);

	data_output += 2;

	for(i=0;i<output_dim_c;i++){
		data_output[i] = total_offset;
		if(data_bias)
			data_output[i] += data_bias[i];
	}

	for(i = 0; i<output_dim_c; i++){
		for(j=0;j<filter_dim_n;j++){
			data_output[i] += data_filter[j*output_dim_c + i] * input_offset;
		}
	}

#ifdef ZSP_NN_DUMP

        char mask_out[12] = {1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
        zsp_nn_dump_parameters(
            TFLM_FULLY_CONNECTED_PREPROCESS_PARAMS_LIST_NAMES, 12,
            "fully_connected_preprocess_s8", "out", mask_out);
#endif

}
