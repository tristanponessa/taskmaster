/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_d.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/02/09 19:52:07 by trponess          #+#    #+#             */
/*   Updated: 2018/03/28 18:35:03 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../../includes/ft_printf.h"

void	add_sign(t_option *option, const char *num)
{
	if (num[0] == '-')
		ft_stock_buf('-', ' ', ' ');
	else if (option->plus == 1 && num[0] != '-')
		ft_stock_buf('+', ' ', ' ');
	else if (option->space == 1 && num[0] != '-')
		ft_stock_buf(' ', ' ', ' ');
}

void	add_width(t_option *option, int nb_len, const char *num)
{
	int i;
	int precision;
	int sign;

	if (num[0] != '-' && (option->plus || option->space))
		sign = 1;
	else
		sign = 0;
	if (option->precision < nb_len)
		precision = 0;
	else
		precision = option->precision - nb_len;
	if (num[0] == '0' && option->precision == 0)
		nb_len = 0;
	if (num[0] == '-' && option->precision >= nb_len)
		nb_len++;
	i = nb_len + precision + sign;
	while (i < option->width)
	{
		if (option->zero && !option->minus && option->precision == -1)
			ft_stock_buf('0', ' ', ' ');
		else
			ft_stock_buf(' ', ' ', ' ');
		i++;
	}
}

void	add_number(const char *num, t_option *option, int nb_len)
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

char	*cast_nbd(t_option *option, long nb)
{
	char *num;

	if ((option->type == 'd' || option->type == 'i') && (option->size == 'H'))
		num = long_to_str((char)nb, 10, 's');
	else if ((option->type == 'd' || option->type == 'i')
			&& (option->size == 'h'))
		num = long_to_str((short int)nb, 10, 's');
	else if ((option->type == 'd' || option->type == 'i')
			&& option->size == ' ')
		num = long_to_str((int)nb, 10, 's');
	else if ((option->type == 'd' || option->type == 'i') &&
			(option->size == 'l' || option->size == 'L'))
		num = long_to_str(nb, 10, 's');
	else if (option->type == 'D')
		num = long_to_str(nb, 10, 's');
	else if ((option->type == 'd' || option->type == 'i')
		&& (option->size == 'j'))
		num = long_to_str((intmax_t)nb, 10, 's');
	else if ((option->type == 'd' || option->type == 'i')
		&& (option->size == 'z'))
		num = long_to_str((int)nb, 10, 's');
	else
		num = NULL;
	return (num);
}

int		print_d(t_option *option, va_list args)
{
	long	nb;
	int		nb_len;
	char	*num;

	nb = va_arg(args, long);
	num = cast_nbd(option, nb);
	nb_len = (int)ft_strlen(num);
	if (option->zero && option->precision == -1)
		add_sign(option, num);
	if (!option->minus)
		add_width(option, nb_len, num);
	if (!option->zero || (option->zero && option->precision > -1))
		add_sign(option, num);
	add_number(num, option, nb_len);
	if (option->minus)
		add_width(option, nb_len, num);
	if (num != NULL)
		free(num);
	return (0);
}
