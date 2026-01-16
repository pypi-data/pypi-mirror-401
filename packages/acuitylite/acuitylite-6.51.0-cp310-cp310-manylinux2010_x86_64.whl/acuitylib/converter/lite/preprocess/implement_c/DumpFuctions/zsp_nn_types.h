/*
 * SPDX-FileCopyrightText: Copyright 2020-2024 Arm Limited and/or its affiliates <open-source-office@arm.com>
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the License); you may
 * not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an AS IS BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/* ----------------------------------------------------------------------
 * Project:      ZSP NN Library
 * Title:        zsp_nn_types.h
 * Description:  Public header file to contain the ZSP-NN structs for the
 *               TensorFlowLite micro compliant functions
 *
 * $Date:        6 May 2024
 * $Revision:    V.1.0.0
 *
 *
 * -------------------------------------------------------------------- */

#ifndef ZSP_NN_TYPES_H
#define ZSP_NN_TYPES_H

#include <stdint.h>

/**
 * @defgroup genPubTypes Structure Types
 * @ingroup Public
 * @brief Enums and Data Structures used in public API
 * @{
 */

/** Enum for specifying activation function types */
typedef enum
{
    ZSP_NN_SIGMOID = 0, /**< Sigmoid activation function */
    ZSP_NN_TANH = 1,    /**< Tanh activation function */
} zsp_nn_activation_type;

/** Function return codes */
typedef enum
{
    ZSP_NN_SUCCESS = 0,        /**< No error */
    ZSP_NN_ARG_ERROR = -1,     /**< One or more arguments are incorrect */
    ZSP_NN_NO_IMPL_ERROR = -2, /**<  No implementation available */
    ZSP_NN_FAILURE = -3,       /**<  Logical error */
} zsp_nn_status;

/** ZSP-NN object to contain the width and height of a tile */
typedef struct
{
    int32_t w; /**< Width */
    int32_t h; /**< Height */
} zsp_nn_tile;

/** ZSP-NN object used for the function context. */
typedef struct
{
    void *buf;    /**< Pointer to a buffer needed for the optimization */
    int32_t size; /**< Buffer size */
} zsp_nn_context;

/** ZSP-NN object to contain the dimensions of the tensors */
typedef struct
{
    int32_t n; /**< Generic dimension to contain either the batch size or output channels.
                     Please refer to the function documentation for more information */
    int32_t h; /**< Height */
    int32_t w; /**< Width */
    int32_t c; /**< Input channels */
} zsp_nn_dims;

/** ZSP-NN object to contain LSTM specific input parameters related to dimensions */
typedef struct
{
    int32_t max_time;
    int32_t num_inputs;
    int32_t num_batches;
    int32_t num_outputs;
} zsp_nn_lstm_dims;

/** ZSP-NN object for the per-channel quantization parameters */
typedef struct
{
    int32_t *multiplier; /**< Multiplier values */
    int32_t *shift;      /**< Shift values */
} zsp_nn_per_channel_quant_params;

/** ZSP-NN object for the per-tensor quantization parameters */
typedef struct
{
    int32_t multiplier; /**< Multiplier value */
    int32_t shift;      /**< Shift value */
} zsp_nn_per_tensor_quant_params;

/** ZSP-NN object for the quantized Relu activation */
typedef struct
{
    int32_t min; /**< Min value used to clamp the result */
    int32_t max; /**< Max value used to clamp the result */
} zsp_nn_activation;

/** ZSP-NN object for the convolution layer parameters */
typedef struct
{
    int32_t input_offset;  /**< The negative of the zero value for the input tensor */
    int32_t output_offset; /**< The negative of the zero value for the output tensor */
    zsp_nn_tile stride;
    zsp_nn_tile padding;
    zsp_nn_tile dilation;
    zsp_nn_activation activation;
} zsp_nn_conv_params;

/** ZSP-NN object for the transpose convolution layer parameters */
typedef struct
{
    int32_t input_offset;  /**< The negative of the zero value for the input tensor */
    int32_t output_offset; /**< The negative of the zero value for the output tensor */
    zsp_nn_tile stride;
    zsp_nn_tile padding;
    zsp_nn_tile padding_offsets;
    zsp_nn_tile dilation;
    zsp_nn_activation activation;
} zsp_nn_transpose_conv_params;

/** ZSP-NN object for the depthwise convolution layer parameters */
typedef struct
{
    int32_t input_offset;  /**< The negative of the zero value for the input tensor */
    int32_t output_offset; /**< The negative of the zero value for the output tensor */
    int32_t ch_mult;       /**< Channel Multiplier. ch_mult * in_ch = out_ch */
    zsp_nn_tile stride;
    zsp_nn_tile padding;
    zsp_nn_tile dilation;
    zsp_nn_activation activation;
} zsp_nn_dw_conv_params;

/** ZSP-NN object for pooling layer parameters */
typedef struct
{
    zsp_nn_tile stride;
    zsp_nn_tile padding;
    zsp_nn_activation activation;
} zsp_nn_pool_params;

/** ZSP-NN object for Fully Connected layer parameters */
typedef struct
{
    int32_t input_offset;  /**< The negative of the zero value for the input tensor */
    int32_t filter_offset; /**< The negative of the zero value for the filter tensor. Not used */
    int32_t output_offset; /**< The negative of the zero value for the output tensor */
    zsp_nn_activation activation;
} zsp_nn_fc_params;

/** ZSP-NN object for SVDF layer parameters */
typedef struct
{
    int32_t rank;
    int32_t input_offset;  /**< The negative of the zero value for the input tensor */
    int32_t output_offset; /**< The negative of the zero value for the output tensor */
    zsp_nn_activation input_activation;
    zsp_nn_activation output_activation;
} zsp_nn_svdf_params;

/** ZSP-NN object for Softmax s16 layer parameters */
typedef struct
{
    const int16_t *exp_lut;
    const int16_t *one_by_one_lut;
} zsp_nn_softmax_lut_s16;

/** ZSP-NN object for quantization parameters */
typedef struct
{
    int32_t multiplier; /**< Multiplier value */
    int32_t shift;      /**< Shift value */
} zsp_nn_scaling;

/** ZSP-NN object for LSTM gate parameters*/
typedef struct
{
    int32_t input_multiplier;
    int32_t input_shift;
    const int8_t *input_weights;
    const int32_t *input_effective_bias; /**< Bias added with precomputed kernel_sum * lhs_offset*/

    int32_t hidden_multiplier;
    int32_t hidden_shift;
    const int8_t *hidden_weights;
    const int32_t *hidden_effective_bias; /**< Precomputed kernel_sum * lhs_offset*/

    const int32_t *bias;
    zsp_nn_activation_type activation_type;
} zsp_nn_lstm_gate;

/** ZSP-NN object for LSTM parameters*/
typedef struct
{
    int32_t time_major; /**< 0 if first dimension is batch, else first dimension is time */
    int32_t batch_size;
    int32_t time_steps;
    int32_t input_size; /**< Size of new data input into the LSTM cell*/
    int32_t
        hidden_size; /**< Size of output from the LSTM cell, used as output and recursively into the next time step*/

    int32_t input_offset;

    int32_t forget_to_cell_multiplier;
    int32_t forget_to_cell_shift;
    int32_t input_to_cell_multiplier;
    int32_t input_to_cell_shift;
    int32_t cell_clip; /**< Min/max value of cell output*/
    int32_t cell_scale_power;

    int32_t output_multiplier;
    int32_t output_shift;
    int32_t output_offset;

    zsp_nn_lstm_gate forget_gate;
    zsp_nn_lstm_gate input_gate;
    zsp_nn_lstm_gate cell_gate;
    zsp_nn_lstm_gate output_gate;
} zsp_nn_lstm_params;

/** ZSP-NN object for LSTM scratch buffers*/
typedef struct
{
    void *temp1;
    void *temp2;
    void *cell_state;
} zsp_nn_lstm_context;

typedef struct
{
	int64_t *quantizer;
	int32_t *pre_sum;
}zsp_nn_priv_params;

/**
 * @} // end group genPubTypes
 */

#endif /* ZSP_NN_TYPES_H */
