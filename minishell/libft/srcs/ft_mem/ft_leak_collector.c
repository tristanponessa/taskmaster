/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_leak_collector.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/05/04 19:26:14 by trponess          #+#    #+#             */
/*   Updated: 2018/10/04 17:23:29 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

void	ft_leak_collector(char *data, char *option)
{
	static char		*mels[100000];
	static int		pos;

	if (ft_strcmp(option, "save") == 0)
	{
		mels[pos] = data;
		pos++;
	}
	if (ft_strcmp(option, "free") == 0)
	{
		pos--;
		while (pos >= 0)
		{
			if (mels[pos])
				free(mels[pos]);
			mels[pos] = NULL;
			pos--;
		}
	}
}

void	ft_leak_dcollector(char **p, char *option)
{
	static char		**dmels[100000];
	static int		pos;

	if (ft_strcmp(option, "save") == 0)
	{
		dmels[pos] = p;
		pos++;
	}
	if (ft_strcmp(option, "free") == 0)
	{
		pos--;
		while (pos >= 0)
		{
			if (dmels[pos])
				free(dmels[pos]);
			pos--;
		}
	}
}

void	ft_free(void)
{
	ft_leak_collector(NULL, "free");
	ft_leak_dcollector(NULL, "free");
}
