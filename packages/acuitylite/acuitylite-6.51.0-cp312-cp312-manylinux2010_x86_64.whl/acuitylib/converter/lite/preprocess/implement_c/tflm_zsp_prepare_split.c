#include "tflm_zsp_prepare_split.h"

TfLiteStatus tflm_zsp_prepare_split(int32_t split_axis,
                                int32_t node_num_outputs,
                                int32_t input_type,
                                int32_t input_dims_size,
                                int32_t *input_dims_data,
                                int32_t output0_dims_axis_data,
                                OpDataSplit *data
                                ){

    int32_t axis_value = split_axis;
    int32_t outer_size = 1;
    int32_t base_inner_size = 1;
    int32_t datatype_bytes = tflm_zsp_sizeof_type(input_type);
    int32_t *copy_size = (int32_t *)&data->copy_size0;
    int32_t i = 0;

    if(axis_value < 0)
        axis_value += input_dims_size;

    outer_size = 1;
    for (i = 0; i < axis_value; ++i) {
        outer_size *= input_dims_data[i];
    }

    base_inner_size = 1* datatype_bytes;
    for (i = axis_value + 1; i < input_dims_size; ++i)
    {
        base_inner_size *= input_dims_data[i];
    }

    for (i = 0; i < node_num_outputs; i++)
    {
        copy_size[i] = output0_dims_axis_data * base_inner_size;
    }

    data->output_count = node_num_outputs;
    data->outer_size = outer_size;

    return kTfLiteOk;
}
