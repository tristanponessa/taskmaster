# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: trponess <trponess@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/03/30 11:59:50 by trponess          #+#    #+#              #
#    Updated: 2018/10/09 12:35:09 by trponess         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME:= minishell

SRC_M:= main.c shell.c\
builtin.c builtin_2.c builtin_extra.c\
art.c search.c path.c\
prepare.c prepare_extra.c\
extra.c extra2.c extra3.c

SRC:= $(addprefix src/, ${SRC_M})
OBJ:= $(subst src/,objects/,$(SRC:.c=.o))
LIBFT:= libft/libft.a
FLAGS:= -g3 -Wall -Wextra -Werror -I includes/

all: $(NAME)

$(NAME): $(LIBFT) $(OBJ)
	@printf "\n\e[1;35mCréation du binaire\e[0m - %-50s\n" $@
	@gcc $(FLAGS) -o $(NAME) $(OBJ) $(LIBFT) 

objects/%.o: src/%.c
	@printf "\e[1;31mCréation des .o\e[0m - %-50s\r" $@
	@mkdir -p objects/
	@gcc $(FLAGS) -c $< -o $@

$(LIBFT):
	@make -C libft/

clean:
	@/bin/rm -rf objects/ && \
	make -C libft clean

fclean: clean
	@/bin/rm -f $(NAME) && \
	make -C libft fclean

re: fclean all

.PHONY: all clean fclean re