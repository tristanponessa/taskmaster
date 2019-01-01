# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: trponess <trponess@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/03/30 11:59:50 by trponess          #+#    #+#              #
#    Updated: 2019/01/01 19:43:01 by trponess         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = taskmaster
SRC :=  taskmaster.c \
		mina.c
		

OBJ :=  $(subst src/, objects/, $(SRC:.c=.o))
LIBFT := libft/libft.a
FLAGS := -g3 -I . 
#-g3 -Wall -Wextra -Werror -I .

all: $(NAME)

$(NAME): $(LIBFT) $(OBJ)
	@printf "\n\e[1;35mCréation du binaire\e[0m - %-50s\n" $@
	@gcc $(FLAGS) $(OBJ) $(LIBFT) -o $(NAME) -l termcap

objects/%.o: src/%.c
	@printf "\e[1;31mCréation des .o\e[0m - %-50s\r" $@
	@mkdir -p objects/
	@gcc $(FLAGS) -c $< -o $@

$(LIBFT):
	@make -C libft/

clean:
	@/bin/rm -rf objects/ && \
	make -C libft/ clean

fclean: clean
	@/bin/rm -f $(NAME) && \
	make -C libft fclean && \
	rm -rf $(NAME).dSYM

re: fclean all

.PHONY: all clean fclean re

