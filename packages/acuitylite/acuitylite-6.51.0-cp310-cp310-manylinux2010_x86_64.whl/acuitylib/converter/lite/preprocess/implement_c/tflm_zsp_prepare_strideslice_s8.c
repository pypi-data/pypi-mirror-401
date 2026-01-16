#include "tflm_zsp_prepare_strideslice_s8.h"

static int32_t Clamp(const int v, const int lo, const int hi)
{
    if (hi < v) return hi;
    if (v < lo) return lo;
    return v;
}

static int32_t StridedSliceStartForAxis(
        int32_t input_shape_axis,
        int32_t start_indices_axis,
        int32_t strides_axis,
        int32_t begin_mask,
        int32_t axis)
{
    int32_t axis_size;
    int32_t start;
    int32_t stride;

    axis_size = input_shape_axis;
    start = start_indices_axis;
    stride = strides_axis;
    begin_mask = (begin_mask & 1 << axis);


    if (start < 0) {
        start += axis_size;
    }
    if (stride > 0) {
        start = Clamp(start, 0, axis_size);
    }
    else {
        start = Clamp(start, -1, axis_size - 1);
    }
    if (begin_mask) {
        if (stride > 0) {
            start = 0;
        }
        else {
            start = axis_size - 1;
        }
    }
    return start;
}

static int32_t StridedSliceEndForAxis(
                uint16_t shrink_axis_mask,
                int32_t offset,
                int32_t stop_indices_axis,
                int32_t strides_axis,
                int32_t end_mask,
                int32_t input_shape_axis,
                int32_t axis,
                int32_t start)
{

    int32_t shrink_axis = shrink_axis_mask & (1 << axis);
    int32_t axis_size = input_shape_axis;
    int32_t end = stop_indices_axis;
    int32_t stride = strides_axis;
    end_mask = (end_mask & 1 << axis);

    if (shrink_axis)
    {
        if (start >= axis_size)
        {
            return start;
        }
        else {
            return start + 1;
        }
    }

    if (offset)
    {
        end += start;
    }

    if (end < 0)
    {
        end += axis_size;
    }
    if (stride > 0)
    {
        end = Clamp(end, 0, axis_size);
    }
    else
    {
        end = Clamp(end, -1, axis_size - 1);
    }

    if (end_mask)
    {
        if (stride > 0)
        {
            end = axis_size;
        }
        else
        {
            end = -1;
        }
    }
    return end;
}

TfLiteStatus tflm_zsp_prepare_stridedslice_s8(int32_t* op_context_begin,
    int32_t* op_context_end,
    int32_t* op_context_strides,
    int32_t  op_context_params_begin_mask,
    int32_t  op_context_params_end_mask,
    int32_t  op_context_params_shrink_axis_mask,
    int32_t input_dims_size,
    int32_t *input_dims_data,
    OpDataStridedSlice *data) {

    int32_t start_indices[5];
    int32_t stop_indices[5];

    uint16_t begin_mask = op_context_params_begin_mask;
    uint16_t end_mask = op_context_params_end_mask;
    uint16_t shrink_axis_mask = op_context_params_shrink_axis_mask;
    int32_t offset;

    int32_t dims = input_dims_size;
    int32_t pad_count = 5 - dims;
    int32_t i = 0;
    int32_t *input_shape = (int32_t *)&data->input_shape0;
    int32_t *strides = (int32_t *)&data->strides0;
    int32_t *start = (int32_t *)&data->start0;
    int32_t *stop = (int32_t *)&data->stop0;

    for (i = 0; i < pad_count; ++i)
    {
        start_indices[i] = 0;
        stop_indices[i] = 1;
        strides[i] = 1;
    }

    for (i = dims; i >= 0; --i)
    {
        start_indices[i + pad_count] = op_context_begin[i];
        stop_indices[i + pad_count] = op_context_end[i];
        strides[i + pad_count] = op_context_strides[i];
    }

    offset = 0;
    shrink_axis_mask = shrink_axis_mask << pad_count;
    begin_mask = begin_mask << pad_count;
    end_mask = end_mask << pad_count;
    begin_mask |= (1 << pad_count) - 1;
    end_mask |= (1 << pad_count) - 1;

    for (i = 0; i < pad_count; ++i)
    {
        input_shape[i] = 1;
    }
    for (i = 0; i < dims; i++)
    {
        input_shape[i+ pad_count] = input_dims_data[i];
    }

    for (i = 0; i < 5; i++)
    {
        start[i] = StridedSliceStartForAxis(input_shape[i], start_indices[i], strides[i], begin_mask, i);
        stop[i] = StridedSliceEndForAxis(shrink_axis_mask, offset, stop_indices[i], strides[i], end_mask, input_shape[i], i, start[i]);
    }

    return kTfLiteOk;
}















