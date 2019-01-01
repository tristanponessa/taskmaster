/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tristan <tristan@student.42.fr>            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2018/03/29 05:42:06 by tristan           #+#    #+#             */
/*   Updated: 2018/09/12 10:46:50 by tristan          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "../../includes/libft.h"

int		line_verif(char **line, char **tmp, int res, char **str)
{
	if (res == 0 && ft_strlen(*tmp) > 0)
	{
		*line = *tmp;
		*str = NULL;
		*tmp = NULL;
		return (1);
	}
	if (res == 0 && ft_strlen(*tmp) == 0)
		return (0);
	return (res);
}

char	*read_line(char *tmp)
{
	size_t	t;
	char	*line;

	t = 0;
	while (tmp[t] != '\n')
		t++;
	line = ft_strnew(t);
	line = ft_strncpy(line, tmp, t);
	line[t] = '\0';
	return (line);
}

char	*cpycat(char *s1, char *s2)
{
	char *tmp;

	tmp = NULL;
	if ((s1 && !s2) || (!s1 && s2))
		return (s1 ? s1 : s2);
	if (!s1 && !s2)
		return (NULL);
	tmp = ft_strnew(ft_strlen(s1) + ft_strlen(s2));
	tmp = ft_strcpy(tmp, s1);
	tmp = ft_strncat(tmp, s2, ft_strlen(s2));
	return (tmp);
}

int		get_next_line(int const fd, char **line)
{
	static char		*str;
	int				res;
	char			*buf;
	char			*tmp;

	if (fd < 0 || !line || BUFF_SIZE < 1 || BUFF_SIZE > 10000000)
		return (-1);
	buf = ft_strnew(BUFF_SIZE + 1);
	if (str == NULL)
		str = ft_strnew(BUFF_SIZE);
	tmp = ft_strncpy(ft_strnew(BUFF_SIZE), str, BUFF_SIZE);
	while (!(ft_strchr(tmp, '\n')))
	{
		if ((res = read(fd, buf, BUFF_SIZE)) < 1)
			return (line_verif(line, &tmp, res, &str));
		buf[res] = '\0';
		tmp = cpycat(tmp, buf);
	}
	*line = read_line(tmp);
	if (ft_strchr(tmp, '\n'))
		str = ft_strncpy(str, ft_strchr(tmp, '\n') + 1, BUFF_SIZE);
	return (1);
}
