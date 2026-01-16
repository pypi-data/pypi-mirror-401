#include <stdint.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include "tflm_zsp_prepare_common.h"

void QuantizeMultiplier(double double_multiplier, int32_t* quantized_multiplier,
                        int* shift) {

  if (double_multiplier == 0.) {
    *quantized_multiplier = 0;
    *shift = 0;
    return;
  }

  const double q = frexp(double_multiplier, shift);
  long long q_fixed = (long long)round(q * (1LL<<31));

  if (q_fixed == (1LL << 31)) {
    q_fixed /= 2;
    ++*shift;
  }

  if (*shift < -31) {
    *shift = 0;
    q_fixed = 0;
  }

  *quantized_multiplier = (int32_t)(q_fixed);
}

void QuantizeMultiplierSmallerThanOneExp(double double_multiplier, int32_t* quantized_multiplier,
        int* left_shift){

    if(double_multiplier >= 1.0)
        abort();
    if(double_multiplier <= 0.0)
        abort();

    int shift;
    QuantizeMultiplier(double_multiplier, quantized_multiplier, &shift);

    if(shift > 0)
        abort();

    *left_shift = shift;
}




TfLiteStatus GetQuantizedConvolutionMultipler(float input_param_scale,
                                              float filter_scale,
                                              float output_scale,
                                              double* multiplier) {
  double input_product_scale =
      (double)(input_param_scale * filter_scale);
  *multiplier = input_product_scale / (double)(output_scale);

  return kTfLiteOk;
}


static inline TfLiteStatus Quantize(float scale, int32_t zero_point, float f, int32_t* q)
{
  const float tmp = round(f / scale);
  *q = zero_point + (int32_t)(tmp);
  return kTfLiteOk;
}


TfLiteStatus CalculateActivationRangeQuantizedImpl(
    int32_t activation, int32_t qmin,
    int32_t qmax, float output_param_scale, int32_t output_param_zeropoint, int32_t* act_min, int32_t* act_max)
{

  int32_t tmp_q;
  if (activation == kTfLiteActRelu) {
    Quantize(output_param_scale, output_param_zeropoint, 0.0, &tmp_q);
    *act_min = max(qmin, tmp_q);
    *act_max = qmax;
  } else if (activation == kTfLiteActRelu6) {
    Quantize(output_param_scale, output_param_zeropoint, 0.0, &tmp_q);
    *act_min = max(qmin, tmp_q);
    Quantize(output_param_scale, output_param_zeropoint, 6.0, &tmp_q);
    *act_max = min(qmax, tmp_q);
  } else if (activation == kTfLiteActReluN1To1) {
    Quantize(output_param_scale, output_param_zeropoint, -1.0, &tmp_q);
    *act_min = max(qmin, tmp_q);
    Quantize(output_param_scale, output_param_zeropoint, 1.0, &tmp_q);
    *act_max = min(qmax, tmp_q);
  } else {
    *act_min = qmin;
    *act_max = qmax;
  }
  return kTfLiteOk;
}


TfLiteStatus CalculateActivationRangeQuantized(int32_t activation,
                                               int32_t output_type,
                                               float output_param_scale,
                                               int32_t output_param_zeropoint,
                                               int32_t* act_min,
                                               int32_t* act_max)
{
  int32_t qmin = 0;
  int32_t qmax = 0;
  if (output_type == kTfLiteUInt8) {
    qmin = 0;
    qmax = 255;
  } else if (output_type == kTfLiteInt8) {
    qmin = -128;
    qmax = 127;
  } else if (output_type == kTfLiteInt16) {
    qmin = -32768;
    qmax = 32767;
  }

  return CalculateActivationRangeQuantizedImpl(activation, qmin, qmax, output_param_scale, output_param_zeropoint, act_min, act_max);
}

void CalculateActivationRange_s32(int32_t activation,
    int32_t* activation_min,
    int32_t* activation_max) {
    if (activation == kTfLiteActRelu) {
        *activation_min = 0;
        *activation_max = 0x7fffffff;
    }
    else if (activation == kTfLiteActRelu6) {
        *activation_min = 0;
        *activation_max = 6;
    }
    else if (activation == kTfLiteActReluN1To1) {
        *activation_min = -1;
        *activation_max = 1;
    }
    else {
        *activation_min = 0x80000000;
        *activation_max = 0x7fffffff;
    }
}

TfLiteStatus PopulateConvolutionQuantizationParams(int32_t input_type, float input_param_scale, float filter_param_scale, int32_t filter_quant_scale_size, float* filter_quant_scale_data, int32_t output_type, float output_param_scale, int32_t output_param_zeropoint, int32_t activation, int32_t* multiplier, int* shift, int32_t* output_activation_min, int32_t* output_activation_max, int32_t* per_channel_multiplier, int32_t* per_channel_shift, int32_t num_channels)
{

  const bool is_per_channel = filter_quant_scale_size > 1;

  for (int i = 0; i < num_channels; ++i) {
    // If per-tensor quantization parameter is specified, broadcast it along the
    // quantization dimension (channels_out).
    const float scale = is_per_channel ? filter_quant_scale_data[i] : filter_quant_scale_data[0];
    const double filter_scale = (double)(scale);
    const double effective_output_scale = (double)(input_param_scale) *
                                          filter_scale /
                                          (double)(output_param_scale);
    int32_t significand;
    int channel_shift;
    QuantizeMultiplier(effective_output_scale, &significand, &channel_shift);
    per_channel_multiplier[i] = significand;
    per_channel_shift[i] = channel_shift;
  }

  // Populate scalar quantization parameters.
  // This check on legacy quantization parameters is kept only for backward
  // compatibility.
  if (input_type == kTfLiteUInt8) {

    double real_multiplier = 0.0;
    GetQuantizedConvolutionMultipler(input_param_scale, filter_param_scale, output_param_scale, &real_multiplier);
    int exponent;

    // Populate quantization parameters with multiplier and shift.
    QuantizeMultiplier(real_multiplier, multiplier, &exponent);
    *shift = -exponent;
  }
  if (input_type == kTfLiteInt8 || input_type == kTfLiteUInt8 ||
      input_type == kTfLiteInt16) {
    CalculateActivationRangeQuantized(
        activation, output_type, output_param_scale, output_param_zeropoint, output_activation_min,
        output_activation_max);
  }
  return kTfLiteOk;
}

int32_t tflm_zsp_sizeof_type(TfLiteType type)
{
    int32_t bytes = 0;
    switch (type) {
    case kTfLiteFloat32:
    case kTfLiteInt32:
    case kTfLiteUInt32:
        bytes = 4;
        break;
    case kTfLiteUInt8:
    case kTfLiteInt8:
    case kTfLiteBool:
        bytes = 1;
        break;
    case kTfLiteInt64:
    case kTfLiteUInt64:
    case kTfLiteFloat64:
    case kTfLiteComplex64:
        bytes = 8;
        break;
    case kTfLiteInt16:
    case kTfLiteUInt16:
    case kTfLiteFloat16:
        bytes = 2;
        break;
    case kTfLiteComplex128:
        bytes = 16;
        break;
    default:
        break;
    }
    return bytes;
}

