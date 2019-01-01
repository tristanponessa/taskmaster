/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2017/11/22 10:10:05 by trponess          #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

static long		ft_roof(long nb, int option)
{
	long roof;
	long digit;

	roof = 1;
	digit = 1;
	if (nb < 0)
		nb *= -1;
	while (nb / 10 >= roof)
	{
		roof *= 10;
		digit++;
	}
	if (option == 1)
		return (roof);
	else
		return (digit);
}

static void		ft_create_array(long *ln, long *roof, int *i, char *nb)
{
	while (*roof >= 1)
	{
		nb[*i] = ((*ln % (*roof * 10)) / *roof) + 48;
		*roof /= 10;
		(*i)++;
	}
	nb[*i] = '\0';
}

char			*ft_itoa(int n)
{
	char	*nb;
	long	roof;
	int		neg;
	int		i;
	long	ln;

	ln = (long)n;
	i = 0;
	roof = ft_roof(ln, 1);
	neg = 0;
	if (ln < 0)
	{
		neg = 1;
		ln *= -1;
	}
	if (!(nb = (char *)malloc(sizeof(char) * (ft_roof(ln, 2) + neg + 1))))
		return (NULL);
	if (neg == 1 && i == 0)
		nb[i++] = '-';
	ft_create_array(&ln, &roof, &i, nb);
	return (nb);
}
