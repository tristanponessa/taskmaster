/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   libft.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/12 20:03:09 by trponess          #+#    #+#             */
/*   Updated: 2018/09/25 14:04:57 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef LIBFT_H
# define LIBFT_H
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
# include "ft_printf.h"
# define BUFF_SIZE 1000
# define VECTOR_SIZE 64

typedef long long			t_llong;
typedef unsigned char		t_uchar;
typedef unsigned int		t_uint;
typedef unsigned long		t_ulong;
typedef unsigned long long	t_ullong;
typedef intmax_t			t_x;
typedef uintmax_t			t_ux;
typedef long double			t_z;

typedef struct		s_vector
{
	int				*arr;
	int				len;
	int				cap;
}					t_vector;

typedef struct		s_list
{
	int				nb;
	char			ch;
	struct s_list	*next;
	struct s_list	*last;
}					t_list;

typedef struct		s_fds
{
	char			*buf;
	int				fd;
	struct s_fds	*next;
}					t_fds;

typedef struct		s_counter
{
	int				a;
	int				h;
	int				i;
	int				j;
	int				k;
	int				l;
	int				r;
	int				z;
}					t_counter;

char				*long_to_str(long value, int base, char cap);
char				*ulong_to_str(unsigned long value, int base, char cap);
long				str_to_long(const char *str, int str_base);
unsigned long		str_to_ulong(const char *str, int str_base);
char				*ft_itoa(int n);
int					ft_atoi(const char *str);
void				*ft_memset(void *str, int value, int num);
void				*ft_memcpy(void *dst, const void *src, int n);
void				*ft_memccpy(void *dst, const void *src, int c, int n);
void				ft_bzero(void *s, int n);
void				*ft_memmove(void *dst, const void *src, int len);
void				*ft_memchr(const void *s, int c, int n);
int					ft_memcmp(const void *s1, const void *s2, int n);
int					ft_strlen(const char *str);
char				*ft_strdup(const char *src);
char				*ft_strcpy(char *dest, const char *src);
char				*ft_strncpy(char *dest, const char *src, int n);
char				*ft_strcat(char *dest, const char *src);
char				*ft_strncat(char *dest, const char *src, int nb);
int					ft_strlcat(char *dest, const char *src, int size);
char				*ft_strchr(const char *s, int c);
char				*ft_strrchr(const char *s, int c);
int					ft_strstr(const char *str, const char *to_find);
char				*ft_strnstr(const char *str, const char *to_find, int n);
int					ft_strcmp(const char *s1, const char *s2);
int					ft_strncmp(const char *s1, const char *s2, int n);
int					ft_isunicode(wint_t uch);
int					ft_isalpha(int c);
int					ft_iscap(int ch);
int					ft_isdigit(int c);
int					ft_isalnum(int c);
int					ft_isascii(int c);
int					ft_isprint(int c);
int					ft_tolower(int c);
int					ft_toupper(int c);
void				*ft_memalloc(int size);
void				ft_memdel(void **ap);
char				*ft_strnew(int size);
void				ft_strclr(char *s);
void				ft_striter(char *s, void (*f)(char *));
void				ft_striteri(char *s, void (*f)(unsigned int, char *));
char				*ft_strmap(char const *s, char (*f)(char));
char				*ft_strmapi(char const *s, char (*f)(unsigned int, char));
int					ft_strequ(char const *s1, char const *s2);
int					ft_strnequ(char const *s1, char const *s2, int n);
char				*ft_strsub(char const *s, unsigned int start, int len);
char				*ft_strjoin(char *s1, char *s2);
char				*ft_strtrim(char const *s);
void				ft_putnbr(int nb);
void				ft_putchar(char c);
void				ft_putstr(const char *str);
void				ft_putendl(char const *s);
void				ft_putnbr(int n);
void				ft_putchar_fd(char c, int fd);
void				ft_putstr_fd(char const *s, int fd);
void				ft_putendl_fd(char const *s, int fd);
void				ft_putnbr_fd(int n, int fd);
void				ft_strdel(char **as);
void				lst_add(t_list **list);
t_list				*lst_create_elem();
void				elem_set_value(t_list **list, int n, char c, char mod);
void				lst_to_limit(t_list **list, char limit);
int					lst_len(t_list *list);
char				*lst_to_str(t_list *list);
void				elem_del(t_list **list);
void				lst_del(t_list **list);
void				ft_swap(int *a, int *b);
int					ft_ispower(int n);
int					ft_sqrt(int nb);
char				**ft_create_double_str(int y, int x);
int					**ft_create_double_int(int y, int x);
int					ft_counter(int nb_of_times, char version);
char				*convert_doublechar_to_char(char **tab);
int					ft_open_file(char *file);
int					ft_file_size(char *file);
char				*ft_file_to_str(char *file);
int					get_next_line(const int fd, char **line);
long				ft_do_op(long a, char sign, long b);
void				ft_putarr(int *arr, int nb);
void				ft_putdarr(int **tab, int y, int x);
int					**ft_convert_str_to_doubleint(char *s, int w, int h);
char				**ft_dstrnew(int y, int x);
int					**ft_darrnew(int y, int x);
int					*ft_arrnew(int size);
void				ft_vec_push(t_vector *vec, int n);
void				ft_vec_add(t_vector **vec);
t_vector			*ft_vec_create_elem(void);
void				ft_vec_del(t_vector **list);
int					ft_vec_to_limit(t_vector **list, char *limit);
void				ft_vec_elem_del(t_vector **list);
int					ft_vec_len(t_vector *list);
t_vector			*ft_vec_join(t_vector *v1, t_vector *v2);
void				ft_vec_create_list(t_vector **list, int nb_elem);
int					ft_vec_pos(t_vector *elem);
void				ft_vec_del_tab(t_vector **tab);
void				ft_vec_pos_push(t_vector *vec, int index, int n);
t_vector			*ft_create_vec_tab(int size);
t_vector			*ft_vec_new(void);
void				ft_leak_collector(char *data, char *option);
int					ft_strfind(char *str, char ch);
char				**ft_split_spaces(char *str, char sep);
void				ft_use_args(char ac, char **av, char **env);
int					ft_dstr_find_str(char **separator, char *to_find);
char				*str_most_wanted(char *str, char **sep, char ch);
char				*str_most_wanted_p(char *s, char **f, char c, char *x);
void				ft_putdstr(char **str);
void				ft_putndstr(char **str, int y);
void				ft_putnndstr(char **str, int y, int x);
char				**ft_split_most_wanted(char *s, char **f, char r, char *x);
int					ft_dstrlen(char **dstr);
char				**ft_dstrjoin(char **dstr1, char **dstr2);
char				**ft_tabnew(int y);
char				**ft_dstrdup(char **src);
void				ft_leak_dcollector(char **p, char *option);

#endif
