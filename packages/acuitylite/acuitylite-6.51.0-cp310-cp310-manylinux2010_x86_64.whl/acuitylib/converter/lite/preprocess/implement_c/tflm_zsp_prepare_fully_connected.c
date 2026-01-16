#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include "tflm_zsp_prepare_fully_connected.h"

TfLiteStatus tflm_zsp_prepare_fullyconnected(
								OpDataFullyConnected *data,
								int32_t node_builtin_activation,
								int32_t is_exist_bias,
								const float input_param_scale,
								const float filter_param_scale,
								const float	bias_param_scale,
								const float output_param_scale,
								int32_t input_param_zeropoint,
								int32_t filter_param_zeropoint,
								int32_t output_param_zeropoint
								){

	 const double input_product_scale = (double)input_param_scale * filter_param_scale;
	 double double_multiplier = input_product_scale/(double)output_param_scale;
	 int32_t shift = 0;
	 int32_t q_fixed;
	 int32_t act_min = -128;
	 int32_t act_max = 127;

	 //init param:

	 data->input_zero_point = 0;
	 data->filter_zero_point = 0;
	 data->output_zero_point = 0;
	 data->output_activation_min = -128;
	 data->output_activation_max = 127;
	 data->output_multiplier = 0;
	 data->output_shift = 0;

	 if(is_exist_bias){
		 const double scale_diff = abs(input_product_scale - bias_param_scale);
		 if(scale_diff/output_param_scale > 0.02)
			 return kTfLiteError;
	 }
	 if(input_product_scale < 0)
		 return kTfLiteError;


	QuantizeMultiplier(double_multiplier, &q_fixed, &shift);


	 data->output_multiplier = (int32_t)q_fixed;
	 data->output_shift = shift;
	 data->input_zero_point =  input_param_zeropoint;
	 data->filter_zero_point = filter_param_zeropoint;
	 data->output_zero_point = output_param_zeropoint;


	CalculateActivationRangeQuantized(node_builtin_activation,
											   kTfLiteInt8,
                                               output_param_scale,
											   output_param_zeropoint,
                                               &act_min,
                                               &act_max);


	data->output_activation_min = act_min;
	data->output_activation_max = act_max;

	return kTfLiteOk;
}






































