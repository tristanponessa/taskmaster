/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   extra_functions.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tristan <tristan@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/08 16:18:01 by trponess          #+#    #+#             */
/*   Updated: 2018/09/25 20:42:43 by tristan          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../../includes/ft_printf.h"

char	*ft_str_clean(char *str, int size)
{
	int i;

	i = 0;
	while (i < size)
	{
		str[i] = '\0';
		i++;
	}
	return (str);
}

char	*ft_str_set_value(char *str, char value, int size)
{
	int i;

	i = 0;
	while (i < size)
	{
		str[i] = value;
		i++;
	}
	return (str);
}

int		catch_fd(int fd, int save)
{
	static int cfd;

	if (save == 1)
		cfd = fd;
	return (cfd);
}

int		ft_stock_buf(unsigned char c, char node, char show)
{
	static unsigned char	buf[BUFF_SIZE];
	static int				i;
	static int				nb_ch;

	if (show == 's')
	{
		write(1, buf, i);
		return (nb_ch);
	}
	if (node == 'r')
	{
		nb_ch = 0;
		i = 0;
		return (nb_ch);
	}
	if (i == BUFF_SIZE)
	{
		write(catch_fd(0, 0), buf, BUFF_SIZE);
		i = 0;
	}
	buf[i] = c;
	i += 1;
	nb_ch += 1;
	return (nb_ch);
}
