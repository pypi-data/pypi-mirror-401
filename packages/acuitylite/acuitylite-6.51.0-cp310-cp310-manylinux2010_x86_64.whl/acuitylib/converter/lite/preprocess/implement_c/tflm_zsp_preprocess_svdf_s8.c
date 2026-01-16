#include "tflm_zsp_preprocess_common.h"
#include "tflm_zsp_preprocess_svdf_s8.h"
#include <string.h>

#ifdef ZSP_NN_DUMP
#include "zsp_nn_dump.h"
#endif

void tflm_zsp_filter_trans_int8_svdf(int8_t *weights_feature_data, int8_t *weights_feature_transpose_data,
									int8_t *weights_time_data, int8_t *weights_time_transpose_data,
									int32_t weights_feature_dims_n, int32_t input_dims_h,
									int32_t weights_time_dims_h,int32_t svdf_params_rank){

#ifdef ZSP_NN_DUMP

		dump_para_t TFLM_SVDF_FILTER_TRANS_TRANS_PARAMS_LIST_NAMES[8] =
				{ {"weights_feature_data", PARATYPE_POINTER,
					weights_feature_data,
					input_dims_h * weights_feature_dims_n},
				{"weights_time_data", PARATYPE_POINTER, weights_time_data,
					weights_time_dims_h * weights_feature_dims_n},
				{"weights_feature_dims_n", PARATYPE_INT32,
					&weights_feature_dims_n},
				{"input_dims_h", PARATYPE_INT32, &input_dims_h},
				{"weights_time_dims_h", PARATYPE_INT32,
					&weights_time_dims_h},
				{"svdf_params_rank", PARATYPE_INT32, &svdf_params_rank},
				{"weights_feature_transpose_data", PARATYPE_POINTER,
					weights_feature_transpose_data,
					input_dims_h * weights_feature_dims_n},
				{"weights_time_transpose_data", PARATYPE_POINTER,
					weights_time_transpose_data,
					weights_time_dims_h * weights_feature_dims_n}
		};

		  char mask[8] = {1,1,1,1,1,1,0,0};
		  zsp_nn_dump_parameters(TFLM_SVDF_FILTER_TRANS_TRANS_PARAMS_LIST_NAMES, 8,
                                      "svdf_filter_trans_s8", "in", mask);
#endif

	tflm_zsp_filter_data Src_mat, dst_mat;

	Src_mat.pData = weights_feature_data;
	Src_mat.numRows = weights_feature_dims_n;
	Src_mat.numCols = input_dims_h;

	dst_mat.pData = weights_feature_transpose_data;

	tflm_zsp_mat_trans_int8(&Src_mat, &dst_mat);

	Src_mat.pData = weights_time_data;
	Src_mat.numRows = weights_feature_dims_n/svdf_params_rank;
	Src_mat.numCols = weights_time_dims_h * svdf_params_rank;

	dst_mat.pData = weights_time_transpose_data;

	tflm_zsp_mat_trans_int8(&Src_mat, &dst_mat);


#ifdef ZSP_NN_DUMP

        char mask_out[8] = {0, 0, 0, 0, 0, 0, 1, 1};

        zsp_nn_dump_parameters(TFLM_SVDF_FILTER_TRANS_TRANS_PARAMS_LIST_NAMES,
                               8, "svdf_filter_trans_s8", "out", mask_out);
#endif

}

void tflm_zsp_preprocess_svdf(int32_t *preprocess_buf ,
							int32_t input_multiplier,
							int32_t input_shift,
							int32_t output_multiplier,
							int32_t output_shift,
							int32_t input_type,
							int32_t output_offset){

#ifdef ZSP_NN_DUMP

          dump_para_t TFLM_PREPROCESS_LIST_NAMES[7] = {
              {"ctx_buf", PARATYPE_POINTER, preprocess_buf, 2 * sizeof(int64_t)},
              {"input_multiplier", PARATYPE_INT32, &input_multiplier},
              {"input_shift", PARATYPE_INT32, &input_shift},
              {"output_multiplier", PARATYPE_INT32, &output_multiplier},
              {"output_shift", PARATYPE_INT32, &output_shift},
              {"input_type", PARATYPE_INT32, &input_type},
              {"output_offset", PARATYPE_INT32, &output_offset},

          };

          char mask[10] = {0, 1, 1, 1, 1, 1, 1};

          zsp_nn_dump_parameters(TFLM_PREPROCESS_LIST_NAMES, 7, "svdf_preprocess_s8", "in", mask);
#endif


	memset(preprocess_buf, 0, 2* sizeof(int64_t));

	int32_t input_activation_max = 127;
	int32_t input_activation_min = -128;
	int32_t output_activation_max = 127;
	int32_t output_activation_min = -128;

	if(input_type == kTfLiteInt8)
	{
		input_activation_max = 127;
		input_activation_min = -128;
	}
	if(input_type == kTfLiteInt16)
	{
		input_activation_max = 32767;
		input_activation_min = -32768;
	}

	*(int64_t *)preprocess_buf = tflm_zsp_requantize_int8(input_multiplier,
			input_activation_max,
			input_activation_min,
			0,
			input_shift);


	*((int64_t *)preprocess_buf+1) = tflm_zsp_requantize_int8(output_multiplier,
			output_activation_max,
			output_activation_min,
			output_offset,
			output_shift);


#ifdef ZSP_NN_DUMP
        char mask_out[10] = {1, 0, 0, 0, 0, 0, 0};

        zsp_nn_dump_parameters(TFLM_PREPROCESS_LIST_NAMES, 7,
                               "svdf_preprocess_s8", "out", mask_out);
#endif

}
