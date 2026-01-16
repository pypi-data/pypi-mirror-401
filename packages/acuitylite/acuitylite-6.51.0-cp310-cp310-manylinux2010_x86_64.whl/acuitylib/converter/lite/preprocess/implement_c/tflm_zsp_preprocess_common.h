#ifndef __TFLM_ZSP_PREPROCESS_COMMON_H__
#define __TFLM_ZSP_PREPROCESS_COMMON_H__

#include <stdint.h>

typedef struct
{
	uint16_t numRows;     /**< number of rows of the matrix.     */
	uint16_t numCols;     /**< number of columns of the matrix.  */
	int8_t *pData;         /**< points to the data of the matrix. */
} tflm_zsp_filter_data;

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


void tflm_zsp_mat_trans_int8(const tflm_zsp_filter_data * pSrc,const tflm_zsp_filter_data * pDst);
int64_t tflm_zsp_requantize_int8(int32_t multiplier,
		int32_t max,
		int32_t min,
		int32_t output_offset,
		int32_t shift);

void tflm_zsp_convert_nhwc_to_nchw(int8_t* src, int8_t* dst, int32_t n,
                                   int32_t h, int32_t w, int32_t c);


#endif
