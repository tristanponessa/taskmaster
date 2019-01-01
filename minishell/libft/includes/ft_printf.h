/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/01/23 17:52:26 by trponess          #+#    #+#             */
/*   Updated: 2018/09/24 17:24:27 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H
# include <unistd.h>
# include <stdlib.h>
# include <string.h>
# include <stdio.h>
# include <fcntl.h>
# include <stdarg.h>
# include <stdint.h>
# include <limits.h>
# include <wchar.h>
# include <stdint.h>
# include <stddef.h>
# include <locale.h>
# include "libft.h"
# define KNRM "\x1B[0m"
# define KRED "\x1B[31m"
# define KGRN "\x1B[32m"
# define KYEL "\x1B[33m"
# define KBLU "\x1B[34m"
# define KPUR "\x1B[35m"
# define KCYN "\x1B[36m"
# define KWHT "\x1B[37m"

typedef struct	s_option
{
	int			plus;
	int			minus;
	int			space;
	int			hash;
	int			zero;
	int			width;
	int			precision;
	char		size;
	char		type;
}				t_option;

void			add_widths(t_option *option, int nb_len);
void			add_string(t_option *option, const char *num);
int				print_unicode_c(t_option *option, va_list args);
int				print_unicode_s(t_option *option, va_list args);
int				ft_atoi_base(const char *str, int str_base);
int				ft_printf(const char *str, ...);
int				ft_fprintf(int fd, const char *str, ...);
int				check_stock_input(const char *str, int *i, t_option *option);
char			*ulong_to_str(unsigned long value, int base, char cap);
char			*long_to_str(long value, int base, char cap);
int				ft_stock_buf(unsigned char c, char reset, char show);
int				ft_stock_unicode_buf(unsigned char uch, char reset, char show);
char			*stock_param_type_get_nb(t_option *option, va_list args);
int				print_c(t_option *option, va_list args);
int				print_s(t_option *option, va_list args);
int				print_d(t_option *option, va_list args);
int				print_o(t_option *option, va_list args);
int				print_x(t_option *option, va_list args);
void			print_p(t_option *option, va_list args);
int				print_d(t_option *option, va_list args);
int				print_u(t_option *option, va_list args);
int				print_unicode(t_option *option, va_list args, char optionn);
char			*ft_str_clean(char *str, int size);
char			*ft_str_set_value(char *str, char value, int size);
int				ft_isblank(char c);
int				isvalid(char c, int base);
int				ft_atoi_base(const char *str, int str_base);
void			add_widthss(t_option *option, int nb_len);
int				ft_unicode_len(wchar_t *ustr);
char			*create_arch(int archetype_size, char *uch_bin);
int				archetype_size(int bitn, char option);
char			*uch_to_bin(wint_t uch);
wchar_t			*set_s(char optionn, va_list args);
void			u_uni(t_option *option, wchar_t *ustr);
char			*go(int archetype_size, char *archetype, char *uch_bin);
void			add_sign_x(t_option *option, const char *num);
void			add_number_x(const char *num, t_option *option, int nb_len);
void			add_width_x(t_option *option, int nb_len, const char *num);
char			*cast_nbx(t_option *option, long nb);
void			write_unich(char *archetype, int archetype_size);
int				ft_atoi_base(const char *str, int str_base);
int				catch_fd(int fd, int save);

#endif
