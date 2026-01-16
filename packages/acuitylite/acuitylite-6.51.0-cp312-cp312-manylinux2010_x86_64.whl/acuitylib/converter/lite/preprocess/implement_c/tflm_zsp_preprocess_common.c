#include "tflm_zsp_preprocess_common.h"



void tflm_zsp_mat_trans_int8(const tflm_zsp_filter_data * pSrc,const tflm_zsp_filter_data * pDst){

	int8_t *pIn = pSrc->pData;                      /* input data matrix pointer */
	int8_t *pOut = pDst->pData;                     /* output data matrix pointer */
	int16_t nRows = pSrc->numRows;                /* number of rows */
	int16_t nCols = pSrc->numCols;                /* number of columns */
    uint32_t i, j;             /* Loop counters */
//    vsi_status status;                             /* status of matrix transpose */


//simultaniously get 4 rows;
//if on nanoplusplus, we have pack16to32 instruction, than we can simultaniously get 8 rows;
//method for  column to rows transpose: be suited for columns > rows

    int8_t *pIn0 = pIn ;
    int8_t *pIn1 = pIn0 + nCols;
    int8_t *pIn2 = pIn1 + nCols;
    int8_t *pIn3 = pIn2 + nCols;

    int8_t *pOut0 = pOut ;
    int8_t *pOut1 = pOut0 + nRows;
    int8_t *pOut2 = pOut1 + nRows;
    int8_t *pOut3 = pOut2 + nRows;

	for(j=0;j<nCols/4;j++){
		for(i=0; i<nRows/4; i++){

			*pOut0++ = *pIn0++;
			*pOut0++ = *pIn1++;
			*pOut0++ = *pIn2++;
			*pOut0++ = *pIn3++;

			*pOut1++ = *pIn0++;
			*pOut1++ = *pIn1++;
			*pOut1++ = *pIn2++;
			*pOut1++ = *pIn3++;

			*pOut2++ = *pIn0++;
			*pOut2++ = *pIn1++;
			*pOut2++ = *pIn2++;
			*pOut2++ = *pIn3++;

			*pOut3++ = *pIn0++;
			*pOut3++ = *pIn1++;
			*pOut3++ = *pIn2++;
			*pOut3++ = *pIn3++;


			pIn0 += 4*nCols - 4;
			pIn1 += 4*nCols - 4;
			pIn2 += 4*nCols - 4;
			pIn3 += 4*nCols - 4;

		}

		for(i=0;i<nRows%4; i++ ){
			*pOut0++ = *pIn0++;
			*pOut1++ = *pIn0++;
			*pOut2++ = *pIn0++;
			*pOut3++ = *pIn0++;

			pIn0 += nCols - 4;
		}
		pOut0 += 3*nRows;
		pOut1 += 3*nRows;
		pOut2 += 3*nRows;
		pOut3 += 3*nRows;


		pIn += 4;

		pIn0 = pIn ;
		pIn1 = pIn0 + nCols;
		pIn2 = pIn1 + nCols;
		pIn3 = pIn2 + nCols;

	}

	for(j=0;j<nCols%4; j++ ){

		for(i=0; i<nRows/4; i++){

			*pOut0++ = *pIn0++;
			*pOut0++ = *pIn1++;
			*pOut0++ = *pIn2++;
			*pOut0++ = *pIn3++;

			pIn0 += 4*nCols - 1;
			pIn1 += 4*nCols - 1;
			pIn2 += 4*nCols - 1;
			pIn3 += 4*nCols - 1;

		}

		for(i=0;i<nRows%4; i++ ){
			*pOut0++ = *pIn0++;
			pIn0 += nCols - 1;
		}

		pIn += 1;

		pIn0 = pIn ;
		pIn1 = pIn0 + nCols;
		pIn2 = pIn1 + nCols;
		pIn3 = pIn2 + nCols;

	}
}

int64_t tflm_zsp_requantize_int8(int32_t multiplier,
		int32_t max,
		int32_t min,
		int32_t output_offset,
		int32_t output_shift){


	int64_t quantize_value;

	quantize_value = (int64_t)((uint32_t)multiplier >> 16);
	quantize_value |= (int64_t)((min& 0xff)<<16);
	quantize_value |= (int64_t)(max& 0xff)<<24;
	quantize_value |= (int64_t)(output_offset&0xff)<<32;

	if(output_shift + 1 < 0)
		quantize_value |= (((int64_t)((-(output_shift + 1))&0x1f)<<43));
	else
		quantize_value |= (((int64_t)(((output_shift + 1))&0x7)<<40));

	return quantize_value;
}

void tflm_zsp_convert_nhwc_to_nchw(int8_t* src, int8_t* dst, int32_t n,
                                   int32_t h, int32_t w, int32_t c) {
  int32_t i_n, i_h, i_w, i_c;
  int8_t* src_ptr;
  int8_t* dst_ptr;

  for (i_n = 0; i_n < n; i_n++) {
    dst_ptr = dst;
    src_ptr = src;
    for (i_c = 0; i_c < c; i_c++) {
      for (i_h = 0; i_h < h; i_h++) {
        for (i_w = 0; i_w < w; i_w++) {
          *dst_ptr++ = *(src_ptr + i_h * w * c + i_w * c + i_c);
        }
      }
    }
    src += h * w * c;
    dst += h * w * c;
  }
}



