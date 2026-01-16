#include "tflm_zsp_prepare_softmax.h"
#include <math.h>
#include <stdlib.h>


void QuantizeMultiplierGreaterThanOne(double double_multiplier,
                                      int32_t* quantized_multiplier,
                                      int* left_shift) {

	if(double_multiplier <= 1.)
		abort();

	QuantizeMultiplier(double_multiplier, quantized_multiplier, left_shift);

	if(*left_shift < 0)
		abort();
}

void PreprocessSoftmaxScaling(double beta, double input_scale, int input_integer_bits,
						int32_t* quantized_multiplier, int* left_shift){

	const double max_real_multiplier = (1LL << 31) - 1.0;

	const double input_beta_real_multiplier =
					fmin(beta * input_scale * (1 << (31 - input_integer_bits)),
					 max_real_multiplier);


	QuantizeMultiplierGreaterThanOne(input_beta_real_multiplier,
                                   quantized_multiplier, left_shift);


}

int CalculateInputRadius(int input_integer_bits, int input_left_shift,
                         int total_signed_bits) {


	const double max_input_rescaled =
    1.0 * ((1 << input_integer_bits) - 1) *
    (1LL << (total_signed_bits - input_integer_bits)) /(1LL << input_left_shift);


	return floor(max_input_rescaled);


}



TfLiteStatus tflm_zsp_prepare_softmax(
							SoftmaxParams *op_data,
							TfLiteSoftmaxParams params,
							int32_t input_type,
							int32_t output_type,
							const float input_params_scale,
							const float output_params_scale,
							int output_params_zeropoint){

	int input_left_shift;

	if(input_type == kTfLiteUInt8)
		return kTfLiteOk;

	if(output_type == kTfLiteInt16)	{
		if(output_params_zeropoint != -32768)
			return kTfLiteError;

		if(fabs(output_params_scale - 1.0f/65536) > 0.001f * 1.0f/65536)
			return kTfLiteError;

	}else{

		if(output_params_zeropoint != -128)
			return kTfLiteError;

		if(output_params_scale != 1.0f/256)
			return kTfLiteError;
	}

	const int kScaledDiffIntegerBits = 5;
	int total_signed_bits = 31;


	PreprocessSoftmaxScaling(params.beta, (double)input_params_scale, (int)kScaledDiffIntegerBits,
						&op_data->input_multiplier, &input_left_shift);

	op_data->input_left_shift = input_left_shift;

	op_data->diff_min = -1.0 * CalculateInputRadius(kScaledDiffIntegerBits,
                                              op_data->input_left_shift, total_signed_bits);

	return kTfLiteOk;

}
