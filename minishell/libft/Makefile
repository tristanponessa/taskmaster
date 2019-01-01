# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: trponess <trponess@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2016/11/04 17:08:23 by agrumbac          #+#    #+#              #
#    Updated: 2018/09/25 14:16:59 by trponess         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

############################## VAR #############################################

NAME = libft.a

CC = gcc

CFLAGS = -g3 -Wall -Wextra -Werror

############################## SRC #############################################

SRC_IO = \
ft_putendl.c ft_putnbr_fd.c \
ft_putchar.c ft_putendl_fd.c ft_putstr.c \
ft_putchar_fd.c ft_putnbr.c ft_putstr_fd.c\
ft_putarr.c ft_putdarr.c ft_putdstr.c

SRC_LST = \
elem_del.c elem_set_value.c lst_add.c lst_create_elem.c\
lst_del.c lst_len.c lst_to_limit.c lst_to_str.c\
ft_vec_new.c ft_vec_push.c 

SRC_MATHS = \
ft_sqrt.c ft_do_op.c

SRC_MEM = \
ft_bzero.c ft_memccpy.c ft_memcmp.c ft_memdel.c ft_memset.c \
ft_memalloc.c ft_memchr.c ft_memcpy.c ft_memmove.c ft_arrnew.c\
ft_darrnew.c ft_create_double_int.c ft_leak_collector.c

SRC_STR = \
ft_isalnum.c ft_strchr.c ft_strequ.c ft_strmapi.c ft_strrchr.c \
ft_isalpha.c ft_striter.c ft_strncat.c ft_ispower.c\
ft_isascii.c ft_strclr.c ft_striteri.c ft_strncmp.c ft_strstr.c \
ft_isdigit.c ft_strcmp.c ft_strjoin.c ft_strncpy.c ft_strsub.c \
ft_isprint.c ft_strcpy.c ft_strlcat.c ft_strnequ.c ft_strtrim.c \
ft_strdel.c ft_strlen.c ft_strnew.c ft_create_double_str.c ft_tolower.c \
ft_strcat.c ft_strdup.c ft_strmap.c ft_strnstr.c ft_toupper.c \
ft_isunicode.c ft_dstrnew.c ft_split.c ft_str_most_wanted.c \
find.c

SRC_CONVERT = \
ft_convert_doublechar_to_char.c ft_convert_str_to_doubleint.c \
ft_atoi.c ft_itoa.c \
ulong_to_str.c long_to_str.c str_to_long.c str_to_ulong.c\

SRC_CTRL_STRUCT = \
ft_counter.c ft_use_args.c

SRC_FILE = \
ft_file_size.c ft_file_to_str.c ft_open_file.c get_next_line.c

SRC_PRINTF = \
ft_printf.c\
get_stock.c\
print_ch.c\
print_d.c\
print_o.c\
print_p.c\
print_s.c\
print_u.c\
print_x.c\
unicode.c\
extra_functions.c

SRC = \
	$(addprefix srcs/ft_maths/, ${SRC_MATHS}) \
	$(addprefix srcs/ft_lst/, ${SRC_LST}) \
	$(addprefix srcs/ft_mem/, ${SRC_MEM}) \
	$(addprefix srcs/ft_str/, ${SRC_STR}) \
	$(addprefix srcs/ft_convert/, ${SRC_CONVERT}) \
	$(addprefix srcs/ft_ctrl_struct/, ${SRC_CTRL_STRUCT}) \
	$(addprefix srcs/ft_file/, ${SRC_FILE}) \
	$(addprefix srcs/ft_io/ft_printf/, ${SRC_PRINTF}) \
	$(addprefix srcs/ft_io/, ${SRC_IO}) 

COBJ = $(SRC:.c=.o)

OBJ = $(COBJ:.s=.o)

############################## COLORS ##########################################

R = "\033[31m"
G = "\033[32m"
B = "\033[34m"
X = "\033[0m"

############################## BUILD ###########################################

.SILENT:

all: ${NAME}

${NAME}: ${OBJ}
	@echo ${B}Compiling" "[${NAME}]...${X}
	ar rcs ${NAME} ${OBJ}
	@echo ${G}Success"   "[${NAME}]${X}

############################## MORE ############################################

clean:
	@echo ${R}Cleaning"  "[objs]...${X}
	/bin/rm -f ${OBJ}

fclean: clean
	@echo ${R}Cleaning"  "[${NAME}]...${X}
	/bin/rm -f ${NAME}

re: fclean all

.PHONY: all clean fclean re