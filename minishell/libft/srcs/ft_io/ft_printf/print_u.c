/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_u.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/02/22 21:17:49 by trponess          #+#    #+#             */
/*   Updated: 2018/03/28 18:35:03 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../../includes/ft_printf.h"

void	add_widthu(t_option *option, int nb_len, const char *num)
{
	int i;
	int precision;
	int sign;

	if (option->plus || option->space || num[0] == '-')
		sign = 1;
	else
		sign = 0;
	if (option->precision < nb_len)
		precision = 0;
	else
		precision = option->precision - nb_len;
	i = nb_len + precision + sign;
	while (i < option->width)
	{
		if (option->zero)
			ft_stock_buf('0', ' ', ' ');
		else
			ft_stock_buf(' ', ' ', ' ');
		i++;
	}
}

void	add_precisionu(t_option *option, int nb_len, const char *num)
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
}

void	add_numberu(const char *num, t_option *option)
{
	int i;

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

char	*cast_nbdu(t_option *option, long nb)
{
	char *num;

	if (option->type == 'U')
		num = ulong_to_str((unsigned long)nb, 10, option->type);
	if ((option->type == 'u') && (option->size == 'H'))
		num = ulong_to_str((unsigned char)nb, 10, option->type);
	else if ((option->type == 'u') && (option->size == 'h'))
		num = ulong_to_str((unsigned short int)nb, 10, option->type);
	else if ((option->type == 'u') && option->size == ' ')
		num = ulong_to_str((unsigned int)nb, 10, option->type);
	else if ((option->type == 'u') &&
			(option->size == 'l' || option->size == 'L'))
		num = ulong_to_str((unsigned long)nb, 10, option->type);
	else if ((option->type == 'u') && (option->size == 'j'))
		num = ulong_to_str((uintmax_t)nb, 10, option->type);
	else if ((option->type == 'u') && (option->size == 'z'))
		num = ulong_to_str((int)nb, 10, option->type);
	return (num);
}

int		print_u(t_option *option, va_list args)
{
	long	nb;
	int		nb_len;
	char	*num;

	nb = va_arg(args, long);
	num = cast_nbdu(option, nb);
	nb_len = (int)ft_strlen(num);
	if (!option->minus)
		add_widthu(option, nb_len, num);
	add_precisionu(option, nb_len, num);
	add_numberu(num, option);
	if (option->minus)
		add_widthu(option, nb_len, num);
	;
	free(num);
	return (0);
}
