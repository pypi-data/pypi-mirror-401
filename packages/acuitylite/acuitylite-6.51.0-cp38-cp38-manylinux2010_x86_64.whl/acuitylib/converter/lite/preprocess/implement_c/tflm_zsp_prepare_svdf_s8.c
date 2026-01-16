#include "tflm_zsp_prepare_svdf_s8.h"
#include "tflm_zsp_prepare_common.h"


TfLiteStatus tflm_zsp_prepare_svdf(OpDataSvdf *data,
									float input_params_scale,
									float weight_feature_params_scale,
									float activation_state_params_scale,
									float weights_time_params_scale,
									float output_params_scale,
									int32_t input_params_zero_point,
									int32_t output_params_zero_point,
									int32_t	activation_state_params_zero_point){

	const double effective_scale_1 = (double)(
			input_params_scale * weight_feature_params_scale /
			activation_state_params_scale);

	const double effective_scale_2 = (double)(activation_state_params_scale *
            weights_time_params_scale / output_params_scale);

	QuantizeMultiplier(effective_scale_1,
			 &(data->effective_scale_1_a),
			 &(data->effective_scale_1_b));

	 QuantizeMultiplier(effective_scale_2,
			 &(data->effective_scale_2_a),
	         &(data->effective_scale_2_b));

	 data->input_zero_point = input_params_zero_point;
	 data->output_zero_point = output_params_zero_point;
	 data->activation_state_zero_point = activation_state_params_zero_point;

	return kTfLiteOk;
}
