#ifndef __TFLM_ZSP_COMMON_H__
#define __TFLM_ZSP_COMMON_H__
#include <stdint.h>

// Possible fused activation functions.
#define max(a,b) ((a>b)?a:b)
#define min(a,b) ((a>b)?b:a)

/// Note that new error status values may be added in future in order to
/// indicate more fine-grained internal states, therefore, applications should
/// not rely on status values being members of the enum.
typedef enum TfLiteStatus {
  /// Success
  kTfLiteOk = 0,

  /// Generally referring to an error in the runtime (i.e. interpreter)
  kTfLiteError = 1,
} TfLiteStatus;

// Possible fused activation functions.
typedef enum {
  kTfLiteActNone = 0,
  kTfLiteActRelu,
  kTfLiteActReluN1To1,  // min(max(-1, x), 1)
  kTfLiteActRelu6,      // min(max(0, x), 6)
  kTfLiteActTanh,
  kTfLiteActSignBit,
  kTfLiteActSigmoid,
} TfLiteFusedActivation;


typedef enum {
  kTfLiteNoType = 0,
  kTfLiteFloat32 = 1,
  kTfLiteInt32 = 2,
  kTfLiteUInt8 = 3,
  kTfLiteInt64 = 4,
  kTfLiteString = 5,
  kTfLiteBool = 6,
  kTfLiteInt16  = 7,
  kTfLiteComplex64 = 8,
  kTfLiteInt8 = 9,
  kTfLiteFloat16 = 10,
  kTfLiteFloat64 = 11,
  kTfLiteComplex128 = 12,
  kTfLiteUInt64 = 13,
  kTfLiteResource = 14,
  kTfLiteVariant = 15,
  kTfLiteUInt32 = 16,
  kTfLiteUInt16 = 17,
  kTfLiteInt4 = 18,
} TfLiteType;


typedef struct {
  int width;
  int height;
  int width_offset;
  int height_offset;
} TfLitePaddingValues;


typedef enum {
  kTfLitePaddingUnknown = 0,
  kTfLitePaddingSame,
  kTfLitePaddingValid,
} TfLitePadding;

TfLiteStatus PopulateConvolutionQuantizationParams(int32_t input_type,
                                                    float input_param_scale,
                                                    float filter_param_scale,
                                                    int32_t filter_quant_scale_size,
                                                    float* filter_quant_scale_data,
                                                    int32_t output_type,
                                                    float output_param_scale,
                                                    int32_t output_param_zeropoint,
                                                    int32_t activation,
                                                    int32_t* multiplier,
                                                    int* shift,
                                                    int32_t* output_activation_min,
                                                    int32_t* output_activation_max,
                                                    int32_t* per_channel_multiplier,
                                                    int32_t* per_channel_shift,
                                                    int32_t num_channels);

TfLiteStatus CalculateActivationRangeQuantized(int32_t activation,
                                               int32_t output_type,
                                               float output_param_scale,
                                               int32_t output_param_zeropoint,
                                               int32_t* act_min,
                                               int32_t* act_max);

void CalculateActivationRange_s32(int32_t activation,
                              int32_t* activation_min,
                              int32_t* activation_max);

void QuantizeMultiplier(double double_multiplier,
                        int32_t* quantized_multiplier,
                        int* shift);

void QuantizeMultiplierSmallerThanOneExp(double double_multiplier,
                        int32_t* quantized_multiplier,
                        int* left_shift);

int32_t tflm_zsp_sizeof_type(TfLiteType type);
#endif
