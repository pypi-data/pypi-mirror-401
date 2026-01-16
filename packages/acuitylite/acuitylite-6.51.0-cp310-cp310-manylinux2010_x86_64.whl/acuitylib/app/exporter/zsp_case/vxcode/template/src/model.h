

#ifndef __MODEL_H__
#define __MODEL_H__


#include "tflm_zsp_graph.h"



int get_tensor_size_by_type(int type);
int tflm_zsp_get_graph_input_size(TFLMZSP_Graph_PTR graph, int input_index);
int tflm_zsp_get_graph_output_size(TFLMZSP_Graph_PTR graph, int output_index);
int tflm_zsp_create_graph(TFLMZSP_Graph_PTR *graph);
void tflm_zsp_destroy_graph(TFLMZSP_Graph_PTR *graph);
int tflm_zsp_process_graph(TFLMZSP_Graph_PTR graph);












#endif // __MODEL_H__
