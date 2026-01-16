#include "tflm_zsp_prepare_average_pool.h"
#include "tflm_zsp_prepare_common.h"
#include "tflm_zsp_padding.h"

TfLiteStatus tflm_zsp_prepare_avgpool(
							OpDataPooling *op_data,
							TfLitePoolParams params,
							int32_t input_height,
							int32_t input_width,
							int32_t output_type,
							float output_param_scale,
							int32_t output_param_zeropoint
							){

	int32_t out_height;
	int32_t out_width;

	op_data->padding = ComputePaddingHeightWidth(
		    params.stride_height, params.stride_width, 1,
		    1, input_height, input_width, params.filter_height,
		    params.filter_width, params.padding, &out_height, &out_width);


	CalculateActivationRangeQuantized(params.activation,
											   output_type,
                                               output_param_scale,
											   output_param_zeropoint,
                                               &op_data->activation_min,
                                               &op_data->activation_max);


	  return kTfLiteOk;
}
