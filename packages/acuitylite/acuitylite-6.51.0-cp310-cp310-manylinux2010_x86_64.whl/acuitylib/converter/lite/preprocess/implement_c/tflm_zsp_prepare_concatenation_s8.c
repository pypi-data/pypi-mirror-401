#include "tflm_zsp_prepare_concatenation_s8.h"

inline int CalculatePositiveAxis(int32_t axis, int32_t output_dims_size) {
    if (axis >= 0) {
        return axis;
    }
    else {
        return output_dims_size + axis;
    }
}

TfLiteStatus tflm_zsp_prepare_concatenation_s8(TfLiteConcatenationParams* params,
                                                int32_t output_type,
                                                int32_t node_inputs_size,
                                                int32_t output_dims_size,
                                                int32_t* output_dims_data,
                                                int32_t* input_dims_axis_data,
                                                OpDataConcatenation *op_params)
{
    int32_t outer_size = 1;
    int32_t datatype_bytes;
    int32_t base_inner_size;
    int32_t axis_value = 0;
    int32_t i = 0;
    int32_t* copy_size = (int32_t *)&op_params->copy_size0;

    switch (output_type) {
        case kTfLiteInt8: {
            axis_value = CalculatePositiveAxis(params->axis, output_dims_size);
            op_params->inputs_count = node_inputs_size;
            break;
        }
        default:
            return kTfLiteError;
    }

    for(i = 0; i < axis_value; ++i){
        outer_size *= output_dims_data[i];
    }

    datatype_bytes = tflm_zsp_sizeof_type(output_type);
    base_inner_size = 1 * datatype_bytes;

    for(i = axis_value + 1; i<output_dims_size; i++){
        base_inner_size *= output_dims_data[i];
    }

    for (i = 0; i < op_params->inputs_count; i++)
    {
        copy_size[i] = input_dims_axis_data[i] * base_inner_size;
    }

    op_params->outer_size = outer_size;
    return kTfLiteOk;
}
