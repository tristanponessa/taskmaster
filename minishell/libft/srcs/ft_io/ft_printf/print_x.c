/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_x.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/08 20:22:14 by trponess          #+#    #+#             */
/*   Updated: 2018/03/28 18:35:03 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../../includes/ft_printf.h"

void	add_width_x(t_option *option, int nb_len, const char *num)
{
	int i;
	int precision;
	int sign;

	if ((option->plus && num[0] != '-') || option->space)
		sign = 1;
	else
		sign = 0;
	if (option->precision < nb_len)
		precision = 0;
	else
		precision = option->precision - nb_len;
	if (num[0] == '0' && option->precision == 0)
		nb_len = 0;
	i = nb_len + precision + sign + (option->hash * 2);
	while (i < option->width)
	{
		if (option->zero && !option->minus && option->precision == -1)
			ft_stock_buf('0', ' ', ' ');
		else
			ft_stock_buf(' ', ' ', ' ');
		i++;
	}
}

void	add_number_x(const char *num, t_option *option, int nb_len)
{
	int i;

	i = 0;
	if (num[0] == '-')
		nb_len -= 1;
	while (i < option->precision - nb_len)
	{
		ft_stock_buf('0', ' ', ' ');
		i++;
	}
	i = 0;
	if (num[0] == '0' && option->precision == 0)
		return ;
	if (num[0] == '-')
		i++;
	while (num[i])
	{
		ft_stock_buf(num[i], '0', '0');
		i++;
	}
}

void	add_hash(t_option *option, const char *num)
{
	if (option->hash && num[0] != '0')
	{
		ft_stock_buf('0', '0', '0');
		if (option->type == 'X')
			ft_stock_buf('X', '0', '0');
		else
			ft_stock_buf('x', '0', '0');
	}
}

char	*cast_nbx(t_option *option, long nb)
{
	char *num;

	if ((option->type == 'x' || option->type == 'X') && (option->size == 'H'))
		num = ulong_to_str((unsigned char)nb, 16, option->type);
	else if ((option->type == 'x' || option->type == 'X') &&
			(option->size == 'h'))
		num = ulong_to_str((unsigned short int)nb, 16, option->type);
	else if ((option->type == 'x' || option->type == 'X') &&
			option->size == ' ')
		num = ulong_to_str((unsigned int)nb, 16, option->type);
	else if ((option->type == 'x' || option->type == 'X') &&
			(option->size == 'l' || option->size == 'L'))
		num = ulong_to_str((unsigned long)nb, 16, option->type);
	else if ((option->type == 'x' || option->type == 'X') &&
			(option->size == 'j'))
		num = ulong_to_str((uintmax_t)nb, 16, option->type);
	else if ((option->type == 'x' || option->type == 'X') &&
			(option->size == 'z'))
		num = ulong_to_str((int)nb, 16, option->type);
	else
		num = NULL;
	return (num);
}

int		print_x(t_option *option, va_list args)
{
	long	nb;
	int		nb_len;
	char	*num;

	nb = 0;
	nb = va_arg(args, unsigned long);
	num = cast_nbx(option, nb);
	nb_len = (int)ft_strlen(num);
	if (num[0] == '0' && option->type != 'p')
		option->hash = 0;
	if (option->zero)
		add_hash(option, num);
	if (!option->minus)
		add_width_x(option, nb_len, num);
	if (!option->zero)
		add_hash(option, num);
	add_number_x(num, option, nb_len);
	if (option->minus)
		add_width_x(option, nb_len, num);
	if ((int)ft_strlen(num) != 0)
		free(num);
	return (0);
}
