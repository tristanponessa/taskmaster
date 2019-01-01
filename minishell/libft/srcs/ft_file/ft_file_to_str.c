/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_file_to_str.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: trponess <trponess@student.42.fr>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/29 03:05:23 by tristan           #+#    #+#             */
/*   Updated: 2018/07/22 19:19:41 by trponess         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

char	*ft_file_to_str(char *file)
{
	char	*str;
	char	ch;
	int		i;
	int		fd;
	int		file_size;

	i = 0;
	file_size = ft_file_size(file);
	fd = ft_open_file(file);
	str = ft_strnew(file_size);
	while (read(fd, &ch, 1) != 0)
	{
		str[i] = ch;
		i++;
	}
	close(fd);
	return (str);
}
