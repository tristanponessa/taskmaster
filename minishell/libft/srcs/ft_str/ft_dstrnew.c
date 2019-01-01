/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_dstrnew.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/04/01 18:05:53 by trponess          #+#    #+#             */
/*   Updated: 2018/09/23 15:41:19 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

char	**ft_dstrnew(int y, int x)
{
	char	**dstr;
	int		i;

	i = 0;
	dstr = (char **)malloc(sizeof(char *) * (y + 1));
	ft_leak_dcollector(dstr, "save");
	if (!dstr)
		return (NULL);
	i = 0;
	while (i < y)
	{
		dstr[i] = ft_strnew(x);
		i++;
	}
	dstr[i] = 0;
	return (dstr);
}
