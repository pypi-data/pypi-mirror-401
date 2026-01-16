#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#if defined(__ZSP_G5__) || defined(__linux__)
#include <sys/unistd.h>
#include <sys/stat.h>
#else
#include <direct.h>
#endif
#include <sys/types.h>
#include <time.h>
#include "zsp_nn_types.h"
#include "zsp_nn_dump.h"


#ifdef ZSP_NN_DUMP

#define MAX_PATH_LENGTH 512
#define FOLDER_MODE (S_IRWXU | S_IRWXG | S_IRWXO)


#define ZSP_NN_DUMP_STRUCT_COMMON_CODE() \
    level++; \
    char tab[10]={0}; \
    zsp_nn_dump_get_tab_by_level(tab, level); \

#define ZSP_NN_DUMP_STRUCT(PARA_NAME, PARA, DUMP_FUNC, TAB, LEVEL) \
{ \
    char *dump_tmp_path = malloc(MAX_PATH_LENGTH+1); \
    sprintf(dump_tmp_path, "%s_%s",dump_base_path, PARA_NAME); \
    fprintf(dump_file, "%s%s:\n", TAB, PARA_NAME); \
    DUMP_FUNC(dump_file, PARA, dump_tmp_path, LEVEL);\
    free(dump_tmp_path); \
} \

#define ZSP_NN_DUMP_POINTER(PARA_NAME, PARA, SIZE, TAB) \
{ \
    char dump_bin_name[MAX_PATH_LENGTH+1]; \
    sprintf(dump_bin_name, "%s_%s"".bin", dump_base_path, PARA_NAME); \
    fprintf(dump_file, "%s%s: %s\n", TAB, PARA_NAME, dump_bin_name); \
    zsp_nn_dump_pointer_data(PARA, SIZE, dump_bin_name); \
} \

#define ZSP_NN_DUMP_VALUE(PARA_NAME, PARA, FORMAT, TAB) \
    fprintf(dump_file, "%s%s: "#FORMAT"\n", TAB, PARA_NAME, PARA);\

#define ZSP_NN_DUMP_VALUE_UINT32(PARA_NAME, PARA, TAB) ZSP_NN_DUMP_VALUE(PARA_NAME, PARA, %u, TAB)
#define ZSP_NN_DUMP_VALUE_UINT64(PARA_NAME, PARA, TAB) ZSP_NN_DUMP_VALUE(PARA_NAME, PARA, %llu, TAB)

#define ZSP_NN_DUMP_VALUE_INT32(PARA_NAME, PARA, TAB) ZSP_NN_DUMP_VALUE(PARA_NAME, PARA, %d, TAB)
#define ZSP_NN_DUMP_VALUE_INT64(PARA_NAME, PARA, TAB) ZSP_NN_DUMP_VALUE(PARA_NAME, PARA, %lld, TAB)

#define ZSP_NN_DUMP_VALUE_FLOAT(PARA_NAME, PARA, TAB) ZSP_NN_DUMP_VALUE(PARA_NAME, PARA, %f, TAB)
#define ZSP_NN_DUMP_VALUE_DOUBLE(PARA_NAME, PARA, TAB) ZSP_NN_DUMP_VALUE(PARA_NAME, PARA, %lf, TAB)
#define ZSP_NN_DUMP_VALUE_SIZE_T(PARA_NAME, PARA, TAB) ZSP_NN_DUMP_VALUE(PARA_NAME, PARA, %ld, TAB)

uint64_t dump_count = 0;
struct tm *time_stamp_format = NULL;
time_t time_stamp;

int zsp_nn_create_dir(char *path)
{
#if defined(__ZSP_G5__) || defined(__linux__)
    int res = mkdir(path, FOLDER_MODE);
#else
    int res = _mkdir(path);
#endif
    return res;
}

void zsp_nn_dump_get_tab_by_level(char *tab_buf, int level)
{
    int i;
    for(i=0; i < level; i++)
    {
        sprintf(tab_buf, "%s\t", tab_buf);
    }
}


void zsp_nn_dump_pointer_data(const void *pointer, int size, char *file_name)
{
    FILE *dump_file = fopen(file_name, "wb");

    fwrite(pointer, 1, size, dump_file);
    fclose(dump_file);
}


//======================= Struct Dump=========================

void zsp_nn_dump_parameters_activation(FILE *dump_file, const zsp_nn_activation *activation, char *dump_base_path, int level)
{
    ZSP_NN_DUMP_STRUCT_COMMON_CODE();

    ZSP_NN_DUMP_VALUE_INT32("min", activation->min, tab);
    ZSP_NN_DUMP_VALUE_INT32("max", activation->max, tab);
}

void zsp_nn_dump_parameters_padding(FILE *dump_file, const zsp_nn_tile *padding, char *dump_base_path, int level)
{
    ZSP_NN_DUMP_STRUCT_COMMON_CODE();

    ZSP_NN_DUMP_VALUE_INT32("pad_x", padding->w, tab);
    ZSP_NN_DUMP_VALUE_INT32("pad_y", padding->h, tab);
}


void zsp_nn_dump_parameters_stride(FILE *dump_file, const zsp_nn_tile *stride, char *dump_base_path, int level)
{
    ZSP_NN_DUMP_STRUCT_COMMON_CODE();

    ZSP_NN_DUMP_VALUE_INT32("stride_x", stride->w, tab);
    ZSP_NN_DUMP_VALUE_INT32("stride_y", stride->h, tab);
}

void zsp_nn_dump_parameters_dilation(FILE *dump_file, const zsp_nn_tile *dilation, char *dump_base_path, int level)
{
    ZSP_NN_DUMP_STRUCT_COMMON_CODE();

    ZSP_NN_DUMP_VALUE_INT32("dilation_x", dilation->w, tab);
    ZSP_NN_DUMP_VALUE_INT32("dilation_y", dilation->h, tab);
}


void zsp_nn_dump_parameters_dims(FILE *dump_file, const zsp_nn_dims *dims, char *dump_base_path, int level)
{
    ZSP_NN_DUMP_STRUCT_COMMON_CODE();

    ZSP_NN_DUMP_VALUE_INT32("n", dims->n, tab);
    ZSP_NN_DUMP_VALUE_INT32("h", dims->h, tab);
    ZSP_NN_DUMP_VALUE_INT32("w", dims->w, tab);
    ZSP_NN_DUMP_VALUE_INT32("c", dims->c, tab);
}


void zsp_nn_dump_parameters_per_tensor_quant_params(FILE *dump_file, const zsp_nn_per_tensor_quant_params *per_tensor_quant_params, char *dump_base_path, int level)
{
    ZSP_NN_DUMP_STRUCT_COMMON_CODE();

    ZSP_NN_DUMP_VALUE_INT32("multiplier", per_tensor_quant_params->multiplier, tab);
    ZSP_NN_DUMP_VALUE_INT32("shift", per_tensor_quant_params->shift, tab);
}

void zsp_nn_dump_parameters_per_channel_quant_params(FILE *dump_file, const zsp_nn_per_channel_quant_params_dump *per_channel_quant_params, char *dump_base_path, int level)
{
	///////////////////////////

    ZSP_NN_DUMP_STRUCT_COMMON_CODE();

    ZSP_NN_DUMP_POINTER("multiplier", per_channel_quant_params->multiplier, per_channel_quant_params->multiplier_size, tab);
    ZSP_NN_DUMP_POINTER("shift", per_channel_quant_params->shift, per_channel_quant_params->shift_size, tab);

}


void zsp_nn_dump_parameters_fc_params(FILE *dump_file, const zsp_nn_fc_params *fc_params, char *dump_base_path, int level)
{
    ZSP_NN_DUMP_STRUCT_COMMON_CODE();

    ZSP_NN_DUMP_VALUE_INT32("input_offset", fc_params->input_offset, tab);
    ZSP_NN_DUMP_VALUE_INT32("filter_offset", fc_params->filter_offset, tab);
    ZSP_NN_DUMP_VALUE_INT32("output_offset", fc_params->output_offset, tab);

    ZSP_NN_DUMP_STRUCT("activation", &fc_params->activation, zsp_nn_dump_parameters_activation, tab, level);
}


void zsp_nn_dump_parameters_pool_params(FILE *dump_file, const zsp_nn_pool_params *pool_params, char *dump_base_path, int level)
{
    ZSP_NN_DUMP_STRUCT_COMMON_CODE();

    ZSP_NN_DUMP_STRUCT("padding", &pool_params->padding, zsp_nn_dump_parameters_padding, tab, level);
    ZSP_NN_DUMP_STRUCT("stride", &pool_params->stride, zsp_nn_dump_parameters_stride, tab, level);
    ZSP_NN_DUMP_STRUCT("activation", &pool_params->activation, zsp_nn_dump_parameters_activation, tab, level);
}

void zsp_nn_dump_parameters_svdf_params(FILE *dump_file, const zsp_nn_svdf_params *svdf_params, char *dump_base_path, int level)
{

    ZSP_NN_DUMP_STRUCT_COMMON_CODE();

    ZSP_NN_DUMP_VALUE_INT32("rank", svdf_params->rank, tab);
    ZSP_NN_DUMP_VALUE_INT32("input_offset", svdf_params->input_offset, tab);
    ZSP_NN_DUMP_VALUE_INT32("output_offset", svdf_params->output_offset, tab);
    ZSP_NN_DUMP_STRUCT("input_activation", &svdf_params->input_activation, zsp_nn_dump_parameters_activation, tab, level);
    ZSP_NN_DUMP_STRUCT("output_activation", &svdf_params->output_activation, zsp_nn_dump_parameters_activation, tab, level);
}

void zsp_nn_dump_parameters_conv_params(FILE *dump_file, const zsp_nn_conv_params *conv_params, char *dump_base_path, int level)
{
    ZSP_NN_DUMP_STRUCT_COMMON_CODE();

    ZSP_NN_DUMP_VALUE_INT32("input_offset", conv_params->input_offset , tab);
    ZSP_NN_DUMP_VALUE_INT32("output_offset", conv_params->output_offset , tab);

    ZSP_NN_DUMP_STRUCT("activation", &conv_params->activation, zsp_nn_dump_parameters_activation, tab, level);
    ZSP_NN_DUMP_STRUCT("padding", &conv_params->padding, zsp_nn_dump_parameters_padding, tab, level);
    ZSP_NN_DUMP_STRUCT("stride", &conv_params->stride, zsp_nn_dump_parameters_stride, tab, level);
    ZSP_NN_DUMP_STRUCT("dilation", &conv_params->dilation, zsp_nn_dump_parameters_dilation, tab, level);
}
void zsp_nn_dump_parameters_depthwise_conv_params(FILE *dump_file, const zsp_nn_dw_conv_params *depthwise_conv_params, char *dump_base_path, int level)
{
    ZSP_NN_DUMP_STRUCT_COMMON_CODE();

    ZSP_NN_DUMP_VALUE_INT32("depthwise multiplier", depthwise_conv_params->ch_mult , tab);
    ZSP_NN_DUMP_VALUE_INT32("input_offset", depthwise_conv_params->input_offset , tab);
    ZSP_NN_DUMP_VALUE_INT32("output_offset", depthwise_conv_params->output_offset, tab);

    ZSP_NN_DUMP_STRUCT("dilation", &depthwise_conv_params->dilation, zsp_nn_dump_parameters_dilation, tab, level);
    ZSP_NN_DUMP_STRUCT("padding", &depthwise_conv_params->padding, zsp_nn_dump_parameters_padding, tab, level);
    ZSP_NN_DUMP_STRUCT("stride", &depthwise_conv_params->stride, zsp_nn_dump_parameters_stride, tab, level);
    ZSP_NN_DUMP_STRUCT("activation", &depthwise_conv_params->activation, zsp_nn_dump_parameters_activation, tab, level);
}


void zsp_nn_dump_parameters_context(FILE *dump_file, const zsp_nn_context *context, char *dump_base_path, int level)
{
    ZSP_NN_DUMP_STRUCT_COMMON_CODE();

    ZSP_NN_DUMP_POINTER("buf", context->buf, context->size, tab);
    ZSP_NN_DUMP_VALUE_INT32("size", context->size, tab);

}

//======================= Struct Dump End=========================

void zsp_nn_dump_parameters(dump_para_t* dump_para_p, int para_nums, char *kernel_name, char* in_or_out, char *mask)
{

    int level = 0;
    char tab[10]={0};

    if(time_stamp_format == NULL)
    {
        time(&time_stamp);
        time_stamp_format = localtime(&time_stamp);
    }

    char *dump_base_path = malloc(MAX_PATH_LENGTH+1);

    sprintf(dump_base_path, "./dump_%04d%02d%02d%02d%02d%02d", time_stamp_format->tm_year+1900, time_stamp_format->tm_mon+1, time_stamp_format->tm_mday,
        time_stamp_format->tm_hour+8, time_stamp_format->tm_min, time_stamp_format->tm_sec);
    zsp_nn_create_dir(dump_base_path);

    sprintf(dump_base_path, "%s/%s", dump_base_path, kernel_name);
    zsp_nn_create_dir(dump_base_path);

    printf("dump_base_path:%s\n", dump_base_path);
    zsp_nn_dump_get_tab_by_level(tab, level);
    sprintf(dump_base_path, "%s/dump_%lld_%s_%s", dump_base_path, dump_count, kernel_name, in_or_out);

    char *dump_file_name = malloc(MAX_PATH_LENGTH+1);
    sprintf(dump_file_name, "%s_params.txt", dump_base_path);
    FILE *dump_file = fopen(dump_file_name, "w");
    free(dump_file_name);

	sprintf(dump_base_path, "%s_bin", dump_base_path);
    int i;
    for(i=0; i<para_nums; i++)
    {
        if(mask == NULL || mask[i] >= 1)
        {
            switch (dump_para_p[i].type)
            {
                case PARATYPE_POINTER:
                    ZSP_NN_DUMP_POINTER(dump_para_p[i].name, dump_para_p[i].value, dump_para_p[i].size, tab);
                    break;

                case PARATYPE_INT8:
                case PARATYPE_INT16:
                case PARATYPE_INT32:
                    ZSP_NN_DUMP_VALUE_INT32(dump_para_p[i].name, *((int32_t*)(dump_para_p[i].value)), tab);
                    break;
                case PARATYPE_INT64:
                    ZSP_NN_DUMP_VALUE_INT64(dump_para_p[i].name, *((int64_t*)(dump_para_p[i].value)), tab);
                    break;

                case PARATYPE_UINT8:
                case PARATYPE_UINT16:
                case PARATYPE_UINT32:
                    ZSP_NN_DUMP_VALUE_UINT32(dump_para_p[i].name, *((uint32_t*)(dump_para_p[i].value)), tab);
                    break;
                case PARATYPE_UINT64:
                    ZSP_NN_DUMP_VALUE_UINT64(dump_para_p[i].name, *((uint64_t*)(dump_para_p[i].value)), tab);
                    break;

                case PARATYPE_SIZE_T:
                    ZSP_NN_DUMP_VALUE_SIZE_T(dump_para_p[i].name, *((size_t*)(dump_para_p[i].value)), tab);
                    break;

                case PARATYPE_FLOAT:
                    ZSP_NN_DUMP_VALUE_FLOAT(dump_para_p[i].name, *((float*)(dump_para_p[i].value)), tab);
                case PARATYPE_DOUBLE:
                    ZSP_NN_DUMP_VALUE_DOUBLE(dump_para_p[i].name, *((double*)(dump_para_p[i].value)), tab);

                case PARATYPE_STRUCT_CONTEXT:
                    ZSP_NN_DUMP_STRUCT(dump_para_p[i].name, (zsp_nn_context*)dump_para_p[i].value, zsp_nn_dump_parameters_context, tab, level);
                    break;

                case PARATYPE_STRUCT_ACTIVATION:
                    ZSP_NN_DUMP_STRUCT(dump_para_p[i].name, (zsp_nn_activation*)dump_para_p[i].value, zsp_nn_dump_parameters_activation, tab, level);
                    break;

                case PARATYPE_STRUCT_DIMS:
                    ZSP_NN_DUMP_STRUCT(dump_para_p[i].name, (zsp_nn_dims*)dump_para_p[i].value, zsp_nn_dump_parameters_dims, tab, level);
                    break;

                case PARATYPE_STRUCT_PER_TENSOR_QUANT_PARAMS:
                    ZSP_NN_DUMP_STRUCT(dump_para_p[i].name, (zsp_nn_per_tensor_quant_params*)dump_para_p[i].value, zsp_nn_dump_parameters_per_tensor_quant_params, tab, level);
                    break;

                case PARATYPE_STRUCT_FC_PARAMS:
                    ZSP_NN_DUMP_STRUCT(dump_para_p[i].name, (zsp_nn_fc_params*)dump_para_p[i].value, zsp_nn_dump_parameters_fc_params, tab, level);
                    break;

                case PARATYPE_STRUCT_POOL_PARAMS:
                	ZSP_NN_DUMP_STRUCT(dump_para_p[i].name, (zsp_nn_pool_params*)dump_para_p[i].value, zsp_nn_dump_parameters_pool_params, tab, level);
                	break;

                case PARATYPE_STRUCT_SVDF_PARAMS:
                	ZSP_NN_DUMP_STRUCT(dump_para_p[i].name, (zsp_nn_svdf_params*)dump_para_p[i].value, zsp_nn_dump_parameters_svdf_params, tab, level);
                	break;
                case PARATYPE_STRUCT_CONV_PARAMS:
                	ZSP_NN_DUMP_STRUCT(dump_para_p[i].name, (zsp_nn_conv_params*)dump_para_p[i].value, zsp_nn_dump_parameters_conv_params, tab, level);
                	break;
                case PARATYPE_STRUCT_DEPTHWISE_CONV_PARAMS:
                	ZSP_NN_DUMP_STRUCT(dump_para_p[i].name, (zsp_nn_dw_conv_params*)dump_para_p[i].value, zsp_nn_dump_parameters_depthwise_conv_params, tab, level);
                	break;
                case PARATYPE_STRUCT_PER_CHANNEL_QUANT_PARAMS:
                	ZSP_NN_DUMP_STRUCT(dump_para_p[i].name, (zsp_nn_per_channel_quant_params_dump*)dump_para_p[i].value, zsp_nn_dump_parameters_per_channel_quant_params, tab, level);
                	break;


                default:
                    break;
            }
        }
    }

    fclose(dump_file);
    free(dump_base_path);
    dump_count++;
}


#endif
