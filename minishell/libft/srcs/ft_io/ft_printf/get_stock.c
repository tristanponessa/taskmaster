/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_stock.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/07 19:40:42 by trponess          #+#    #+#             */
/*   Updated: 2018/03/27 17:12:16 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../../includes/ft_printf.h"

void	get_stock_flag(const char *str, int *i, t_option *option)
{
	while (str[*i])
	{
		if (str[*i] == '0')
			option->zero = 1;
		else if (str[*i] == '+')
			option->plus = 1;
		else if (str[*i] == '-')
			option->minus = 1;
		else if (str[*i] == '#')
			option->hash = 1;
		else if (str[*i] == ' ')
			option->space = 1;
		else
			break ;
		(*i)++;
	}
}

void	get_stock_precision_width(const char *str, int *i, t_option *option)
{
	if (ft_isdigit(str[*i]))
		option->width = ft_atoi(&str[*i]);
	while (ft_isdigit(str[*i]))
		(*i)++;
	if (str[*i] == '.')
	{
		(*i)++;
		if (ft_isdigit(str[*i]))
			option->precision = ft_atoi(&str[*i]);
		while (ft_isdigit(str[*i]))
			(*i)++;
	}
	else
		option->precision = -1;
}

void	get_stock_type(const char *str, int *i, t_option *option)
{
	if (ft_strchr("sSpdDioOuUxXcC%", str[*i]))
		option->type = str[*i];
	else if (str[*i])
		option->type = str[*i];
	if ((option->type == 'c' || option->type == 's') &&
		(option->size == 'l' || option->size == 'L'))
		option->type -= 32;
}

void	get_stock_size(const char *str, int *i, t_option *option)
{
	if (str[*i] == 'h' || str[*i] == 'l' ||
		str[*i] == 'j' || str[*i] == 'z')
	{
		option->size = str[*i];
		(*i)++;
		if ((option->size == 'h' && str[*i] == 'h') ||
			(option->size == 'l' && str[*i] == 'l'))
		{
			option->size -= 32;
			(*i)++;
		}
	}
	else
		option->size = ' ';
}

int		check_stock_input(const char *str, int *i, t_option *option)
{
	ft_bzero(option, sizeof(t_option));
	get_stock_flag(str, i, option);
	get_stock_precision_width(str, i, option);
	get_stock_size(str, i, option);
	get_stock_type(str, i, option);
	return (0);
}
