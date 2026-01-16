CC = gcc
C++ = g++
AR = ar
LD = gcc
RM = rm
MKDIR = mkdir


OPT_FLAGS = -O2
DEBUG_FLAG = -g




MACRO_DEF = 
#MACRO_DEF += -DZSP_NN_DUMP
LIB_FILE = libtflm_zsp_preprocess.so






CFLAGS = $(OPT_FLAGS)
CFLAGS += $(DEBUG_FLAG)
CFLAGS += $(MACRO_DEF)
CFLAGS += -fPIC -shared







OUT_OBJ_DIR = .
OUT_LIB_DIR = ../library





INCLUDE_DIRS = -I./ -IDumpFuctions

C_SOURCE_DIRS = ./ 

 

C_OBJECTS = $(foreach dir, $(C_SOURCE_DIRS), $(patsubst %.c,%.o, $(notdir $(wildcard $(dir)/*.c))))
C_OBJECTS := $(filter-out boot.o, $(C_OBJECTS))
C_OBJECTS := $(addprefix $(OUT_OBJ_DIR)/, $(C_OBJECTS))









VPATH = $(C_SOURCE_DIRS) 


.PHONY : all clean create_dir

all : $(OUT_LIB_DIR)/$(LIB_FILE)
	-$(RM) -f $(OUT_OBJ_DIR)/*.o
	-$(RM) -f $(OUT_OBJ_DIR)/*.d

create_dir :
	-$(MKDIR) $(OUT_LIB_DIR)
	#-$(MKDIR) $(OUT_OBJ_DIR)




-include $(OUT_OBJ_DIR)/*.d


$(OUT_LIB_DIR)/$(LIB_FILE) : $(C_OBJECTS)
	@echo "building $@ start"
	$(CC) -fPIC -shared -o $@ $^ 
	@echo "building $@ finish"


$(C_OBJECTS) : | create_dir



$(C_OBJECTS) : $(OUT_OBJ_DIR)/%.o : %.c
	$(CC) $(CFLAGS) $(INCLUDE_DIRS) -c $< -o $@



clean :
	-$(RM) -f $(OUT_LIB_DIR)/*
	-$(RM) -f $(OUT_OBJ_DIR)/*.o
	-$(RM) -f $(OUT_OBJ_DIR)/*.d

