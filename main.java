
//1ST TEMPTATION OF SHELL PART MINISHELL
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.ObjectInputStream.GetField;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.Map;
import java.util.Properties;
import java.util.Scanner;
import java.io.*;
import java.lang.Object;
import java.text.Format.Field;
import java.util.stream.Collectors;
import java.util.zip.ZipEntry;
import java.util.*;
import java.util.regex.*;
import java.lang.reflect.*;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.*;

class My_color
{
	public final String KNRM = "\u001B[0m";
	public final String KBLK = "\u001B[30m";
	public final String KWHT = "\u001B[37m";
	public final String KRED = "\u001B[31m";
	public final String KBLU = "\u001B[34m";
	public final String KGRN = "\u001B[32m";
	public final String KYEL = "\u001B[33m";
	public final String KPUR = "\u001B[35m";
	public final String KCYN = "\u001B[36m";
	//backround colors
	public final String KBBLK = "\u001B[40m";
	public final String KBRED = "\u001B[41m";
	public final String KBGRN = "\u001B[42m";
	public final String KBYEL = "\u001B[43m";
	public final String KBBLU = "\u001B[44m";
	public final String KBPUR = "\u001B[45m";
	public final String KBCYN = "\u001B[46m";
	public final String KBWHT = "\u001B[47m";
}


class Buildin
{
	public static Command builtin;
	public static LinkedList <String> commands = new LinkedList<>();

	//Main global how to use and save?
	//constructor that tacks adress of main called in main and get its path and save path for cd
	Buildin()
	{
		String[] builtin_names = {"exit", "env", "setenv", "unsetenv", "cd", "cat", "echo", "history"};
		commands.addAll(Arrays.asList(builtin_names));	
	}

	public static void run(Command built) throws IOException
	{//thanks to globals you can use poitors to functions , or a map if "exit" get function.class.name = "exit"
		builtin = built;//reference pass ww wont be modifying it so no problem
		//this could be replaced by class.method table if contains launch function with same name but here you have the freedom to give unik names if needed
		if (builtin.cmd_name.equals("exit")) 		exit();
		if (builtin.cmd_name.equals("env"))  		env();	
		if (builtin.cmd_name.equals("setenv")) 		setenv();
		if (builtin.cmd_name.equals("unsetenv"))  	unsetenv();	
		if (builtin.cmd_name.equals("cd"))			cd();
		if (builtin.cmd_name.equals("cat"))			cat();
		if (builtin.cmd_name.equals("echo"))		echo();
		if (builtin.cmd_name.equals("history"))		history();
		//if (builtin.cmd_name.equals("cat"))  cat();	
	}
	
	//dont forget cat
	
	public static void env()//allow multiple search env setenv unsetenv have the same search for error and executtion loop maybe do a universal thing?
	{
		if (builtin.args.size() == 0)	
			Main.env.forEach((k, v) -> System.out.println(k + "=" + v));
		
		for (String var : builtin.args) 
		{
			if (!Main.env.containsKey(var))
				System.out.println("env : error : " + var + " doesn't exist");
			else
				System.out.println(var + "=" + Main.env.get(var));
		}
	}
	
	public static void setenv()
	{
		
		for (String var : builtin.args) 
		{
			if (!var.matches("^[a-zA-z0-9]+=[a-zA-z0-9]+$"))
			{
				System.out.println("setenv : error : have to respect -> $>setenv [a-zA-z0-9]=[a-zA-z0-9] ...");
				return ;
			}
		}
				
		for (String var : builtin.args) 
		{	
			String[] part = var.split("=");
			Main.env.put(part[0], part[1]);
		}
	}
	
	public static void unsetenv()
	{
		for (String var : builtin.args) 
		{
			if (!Main.env.containsKey(var))
			{
				System.out.println("unsetenv : error : have to respect -> $>unsetenv [a-zA-Z0-9]... AND all the vars must exist");
				return ;
			}
		}
		
		for (String var : builtin.args) 
			Main.env.remove(var);
	}
	
	public static void cd() throws IOException //if earse PWD OLDPWD recreated it
	{//new FILe(path) deals with symbolic links auto
		//i will not except links as curoath paths , it will always be translated
//check if more than one argument
//if yes no cd
		
		String newpath; 
		String oldpath = Main.cur_path.getCanonicalPath(); 
		
		//if one or more paths : wrong
		//check if active same time
		if (!builtin.flag.equals("-") && !builtin.flag.equals("-P") && !builtin.flag.equals("-L"))
		{
			System.out.println("cd : error : option " + builtin.flag + "doesn't exist");
			System.out.println("cd : must be -L or P");
			return ;
		}
		
	//ALL TELEPORTERS cd "" ~ - must have exceptions newpath = the value 
		if (builtin.args.peekFirst() == null)//!!!! IF NO ARGUMENT AFTER CD THIS ACTIVATES OR ELSE ALL YOUR GETFIRST WILL BE IN NOSUCHELEMENT EXCEPTION
			newpath = "/";
		else if (Main.env.containsKey("HOME") && builtin.args.getFirst().equals(Main.env.get("HOME")))
			newpath = Main.env.get("HOME");//~ is exceptional it saids no matter where you are teleport here
		else if (Main.env.containsKey("OLDPWD") && builtin.args.getFirst().equals(Main.env.get("OLDPWD"))) //for cd -
			newpath = Main.env.get("OLDPWD");
		else
			newpath = Main.cur_path.getAbsolutePath() + "/" + builtin.args.getFirst();
		
		File test = new File(newpath);//auto translates ..
		if (test.exists() && test.isDirectory())
		{
			//UNIX SYMBOLIC LINKS ARE GARBAGE THEY NEVER NEVER WORK NOT IN C NOT IN JAVA IN ANY FUCKING LANGUAGE IT SHOULD BE A PROJECT TO ITSELF 
			//BASH JAVA CANT IDENTIFY THE LN -L AND LN I CREATED LOOK UP ON THAT 
			/*if (builtin.flag.equals("-P") && Files.isSymbolicLink(test.toPath()))
			{
				 
				Path realPath = test.toPath();//.toRealPath();//doesnt work shit
				realPath = Files.readSymbolicLink(realPath);
				File z = realPath.toFile();
				newpath = z.getAbsolutePath(); 
			}*/
			
			Main.cur_path = new File(newpath);
			
			if (Main.env.containsKey("PWD"))    Main.env.replace("PWD", Main.cur_path.getCanonicalPath());
			else                                Main.env.put("PWD", newpath);
			
			if (Main.env.containsKey("OLDPWD")) Main.env.replace("OLDPWD", oldpath);
			else                                Main.env.put("OLDPWD", oldpath);
			
		}
		else if (test.exists() && test.isFile())
			System.out.println("cd : error : " + test + " is a file");
		else
			System.out.println("cd : error : " + test + " doesn't exist");
	}
	
	public static void cat() throws IOException//alot of flags ont do them
	{
		boolean wrong = false;
		for (String arg : builtin.args)
		{
			File f = new File(arg);
			if (!f.exists() || !f.isFile())
			{
				System.out.println("cat : error : " + arg + " is not a file");
				wrong = true;
			}
		}
		if (wrong)
		{
			System.out.println("cat : error : incorrect args");
			return ;
		}
		
		for (String arg : builtin.args) 
		{
			File f = new File(arg);
			System.out.println(new String(Files.readAllBytes(Paths.get(f.getPath()))));
		}
		System.out.println("");
	}
	
	public static void echo()
	{
		//E default
		//check if Ee activated at same time
		if (!builtin.flag.equals("-") && !builtin.flag.equals("-n") && !builtin.flag.equals("-e") && !builtin.flag.equals("-E"))
		{
			System.out.println("cd : error : option " + builtin.flag + "doesn't exist");
			System.out.println("cd : must be -n and E or e");
			return ;
		}
		
	
		for (String arg : builtin.args)
		{
			arg = arg.replaceAll("\\\\\"", "--X"); //!!replqce by i,possibl user input chqrqcters
			arg = arg.replaceAll("\"", "--P"); 
			arg = arg.replaceAll("--X", "\"");
			arg = arg.replaceAll("--P", "");
			
			for (int i = 0; i < arg.length(); i++)
			{
				if (builtin.flag.contains("e") && i + 1 < arg.length() && arg.charAt(i) == '\\')
				{
					if (arg.charAt(i + 1) == 'n') System.out.print('\n');
					if (arg.charAt(i + 1) == 't') System.out.print('\t');
					if (arg.charAt(i + 1) == 'b') System.out.print('\b');
					if (arg.charAt(i + 1) == 'r') System.out.print('\r');
					if (arg.charAt(i + 1) == 'f') System.out.print('\f');
					
					i++;
				}
				else
					System.out.print(arg.charAt(i));
			}
			System.out.print(" ");
		}
		
		
		if (!builtin.flag.contains("n"))
			System.out.println();
	}
	
	public static void history() throws IOException//read out log file
	{
		List<String> log_history = Files.readAllLines(Paths.get("./history.txt"));//PERFOMANCE ISSUE its going to read stoxk everytime you call history
		String n;
		
		//if more than one number chain with ; ; or error
		if (builtin.args.size() == 0)
		{
			for (int i = 0; i < log_history.size(); i++) 
			{
				System.out.println(i + ". " + log_history.get(i));
			}		
			System.out.println("which ? : ");
			n = Main.sc.nextLine();
		}
		else
			n = builtin.args.getFirst();//doesnt work 
		
		if (n.matches("[0-9]+") && Integer.valueOf(n) < log_history.size() - 1)//-1 dont work cause n doesnt match - number
		{
		//	if (Integer.valueOf(n) > log_history.size() - 1)
			String old_cmd = log_history.get(Integer.valueOf(n));
			Files.write(Paths.get(System.getProperty("user.dir") + "/history.txt"), (" ->" + old_cmd).getBytes(), StandardOpenOption.APPEND);
			Main.stock_in_cmds(Main.get_input_lines(old_cmd));
		}
		else
			System.out.println("history " + n + " doesn't exist");
	
	}
	
	public static void exit()
	{
		Main.exit_shell = true;//uf you exit here -> unreachable code issue in main
	}

	
}

class Command
{
	public String cmd_name;
	public String cmd_absolutepath;
	public String entire_com = null;
	public String original_com;
	public String flag = "-";
	public LinkedList<String> args;
	public Boolean found;
	public String type = "bin";

	Command(String cmd)
	{
		this.original_com = cmd;//an i messing with references????????????????????????????????????????

		int i = 1;
		String[] parts = cmd.split(" ");
		//String[] parts = cmd.trim().split(" ");
		
		this.cmd_name = parts[0];
		
		this.cmd_absolutepath = Main.get_cmd(cmd_name);//static memebrs are mems pf classes not the object, object m , class main , 

		if (cmd_absolutepath != null && cmd_absolutepath.equals(cmd_name))
			type = "builtin";

		if (cmd_absolutepath != null)	//needed for entire_com
		{
			int n =  cmd_name.indexOf(" ");
			//this.entire_com = cmd_name.substring(0, n == -1 ? cmd_name.length() : n) + cmd_absolutepath;//its cmd.substring(0, last(/)) + cmd --bin/ls -f "F"
			this.entire_com = cmd_absolutepath + original_com.substring(n == -1 ? cmd_name.length() : n);
		}
		
		for ( ;i < parts.length && parts[i].charAt(0) == '-' && parts[i].length() > 1; i++)
			flag += parts[i].substring(1);
		
		args = new LinkedList<>();
		for ( ;i < parts.length; i++)
			args.add(parts[i]);
		
		this.found = (cmd_absolutepath != null) ? true : false; 

		this.type = (!this.found) ? "none" : type;
	}

	public void display_command()
	{
		System.out.println("----------------------------");
		System.out.println("found:" + this.found);
		System.out.println("type:" + this.type);
		System.out.println("orin_comm:" + this.original_com);
		System.out.println("cmd_name:" + this.cmd_name);
		System.out.println("cmd_absoname:" + this.cmd_absolutepath);
		System.out.println("flag:" + this.flag);
		System.out.println("args" + this.args);
		System.out.println("entire_com:" + this.entire_com);
		System.out.println("------------------------------------");
	}

	//Object get_
}

class Main
{

	// java -XshowSettings:properties -version 
	//static public String mingw_env_path = "C:\\Program Files\\Git\\usr\\bin";
	static public Map<String, String> env = 	   new HashMap<>(); //cp[y of env once program done this will be detroyed
	static public File                cur_path =   new File(System.getProperty("user.dir"));//keep file to listfiles ...
	static public LinkedList<File>    exec_dirs =  new LinkedList<>(); //should i put it to null?
	static public LinkedList<Command> cmds =       new LinkedList<>();
	static public Buildin             buildins =   new Buildin();
	static public String[]            input_lines; 
	static public LinkedList<String>  history =     new LinkedList<>();//create a map number command and launch it if person launches hitory //history.exe doesnt exist on mingw
	static public File 				  history_log = new File("history.txt");//exists even after close of session  organise a class that takes care of erasing after certsin time
	//static public File 				  log = new File("log.txt");
 	static public My_color            c = 		   new My_color();
	static public String              os = 		   System.getProperty("os.name");
	static public boolean             is_windows = System.getProperty("os.name").toLowerCase().startsWith("windows");
	static public boolean			  exit_shell = false;
	static public Scanner 				sc;
	
	public static void splash_screen()
	{
		System.out.println(c.KGRN + "           _       _     _          _ _\n" +
				" _ __ ___ (_)_ __ (_)___| |__   ___| | |\n" +
				"| '_ ` _ \\| | '_ \\| / __| '_ \\ / _ \\ | |\n"+
				"| | | | | | | | | | \\__ \\ | | |  __/ | |\n"+
				"|_| |_| |_|_|_| |_|_|___/_| |_|\\___|_|_|\n\n" + c.KNRM);
	}
	
	public static void display_env(int i)
	{
		if (i == 0) env.forEach((k, v) -> System.out.println(c.KBBLU + k + ":" + v + c.KNRM));
		else  
		{
			env.forEach((k, v) -> 
			{
				if (k.equals("HOME") || k.equals("PWD") || k.equals("OLDPWD") || k.equals("PATH")) 
					System.out.println(c.KBBLU + k + ":" + v + c.KNRM);
			});
		}	
	}
	
	public static void display_cmds()
	{
		cmds.forEach((c) -> c.display_command());
	}

	public static void display_builtcomm()
	{
		Buildin.commands.forEach((c) -> System.out.println(c));
	}

	static void add_primary_envvars()
	{
		if (is_windows)
		{
			env.put("PATH", "C:\\Program Files\\Git\\usr\\bin");
			env.put("HOME", System.getenv().get("HOMEPATH"));
		}
		
		if (!env.containsKey("PWD"))
			env.put("PWD", cur_path.getAbsolutePath());
		if (!env.containsKey("OLDPWD"))
			env.put("OLDPWD", cur_path.getParentFile().getAbsolutePath());
	}

	static void get_exec_dirs()
	{
		if (!env.containsKey("PATH") || env.get("PATH").isEmpty())
			return ;
		
		String[] execs;
		if (is_windows) execs = env.get("PATH").split("```");//not allowed to put star tin path
		else       		execs = env.get("PATH").split(":");
		
		for (String exec : execs)
			exec_dirs.add(new File(exec));//cant do this. cant use in a static context...
	}

	static String get_cmd(String cmd)   //PATH class better for flexitibilty or File that acts like path
	{	
		File tmp;
		String[] exclude = {"exit", "env", "setenv", "unsetenv", "cd", "cat", "echo", "history"};
		for (File exec_dir : exec_dirs)//COUNT EXIT AS BUILDIN
		{
			if (Arrays.asList(exclude).contains(cmd)) break;//is a builtin ignore the real exit
			if (is_windows) 		tmp = new File(exec_dir.getAbsolutePath() + "/" + cmd + ".exe");
			else 					tmp = new File(exec_dir.getAbsolutePath() + "/" + cmd);
		
			if (tmp.exists())
				return (tmp.getAbsolutePath());
		}
		
		if (Buildin.commands.contains(cmd))
			return cmd;

		return (null);
	}

	static String[] get_input_lines(String input_line)//everything is trasnlated first
	{//if you cat "~" this will trandlate you must tell regex to ignore
		input_line = input_line.trim().replaceAll("\\s+", " ").replaceAll("\\s*;\\s*", ";");
		
		input_line = input_line.replace("~", env.containsKey("HOME") ? env.get("HOME") : "~");

		Matcher m = Pattern.compile("\\$[A-Za-z0-9]+").matcher(input_line);
		while (m.find())
			input_line = input_line.replace(m.group(), env.containsKey(m.group().substring(1)) ? env.get(m.group().substring(1)) : m.group());

		m = Pattern.compile("cd - ").matcher(input_line);
		while (m.find())
			input_line = input_line.replace(m.group(), env.containsKey("OLDPWD") ?  "cd " + env.get("OLDPWD") : m.group());//the -
			
		input_lines = input_line.split(";");//this.input_lines
		
		return (input_lines);
	}
	
	
	
	static void stock_in_cmds(String[] lines)
	{
		if (lines != null)
			input_lines = lines;
		for (String cmd_piece : input_lines)//this
			cmds.add(new Command(cmd_piece));//here it checks if real comand or not 
	}

	static void launch_command(Command c) throws IOException, URISyntaxException
	{
		if (!c.found)
		{
			System.out.println(c.cmd_name + " doesn't exist");
			return ;
		}

		if (c.type.equals("builtin"))//unessary but clean for eyes
		{
			if (Buildin.commands.contains(c.cmd_name))//HOW TO GET ARGUMENTS?? -> stocked in command
				Buildin.run(c);
		}
		else
		{		
			ProcessBuilder processBuilder = new ProcessBuilder();
			processBuilder.directory(Main.cur_path);//for cd to do a chdir 
			processBuilder.command(c.entire_com.split(" "));//for windows not going to work ////your letting it organise flags and eerything itself //if you want control make fullcommand + pulled together flags

			try {

				Process process = processBuilder.start();
				
				Map<String, BufferedReader> proc_res = new HashMap<>();
				
				proc_res.put("input", new BufferedReader(new InputStreamReader(process.getInputStream())));
				proc_res.put("error", new BufferedReader(new InputStreamReader(process.getErrorStream())));
				
				int exitVal = process.waitFor();
				String x = (exitVal == 0) ? "input" : "error";
				proc_res.get(x).lines().forEach((line) -> System.out.println(line));
				System.out.println();

			} catch (IOException e) {
				e.printStackTrace();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
//just like your cpp projects capture and save when print throw in log to 
	public static void main(String[] args) throws IOException, InterruptedException, FileNotFoundException, URISyntaxException
	{
		/*Terminal terminal = new DefaultTerminalFactory(System.out, System.in, Charset.forName("UTF8")).createTerminal();
		terminal.enterPrivateMode();
	
		terminal.setCursorPosition(10, 5);
		terminal.putCharacter('H');
		terminal.putCharacter('e');
		terminal.putCharacter('l');
		terminal.putCharacter('l');
		terminal.putCharacter('o');
		terminal.putCharacter('!');
		terminal.setCursorPosition(0, 0);*/
		
		//terminal.exitPrivateMode();
		
		splash_screen();
		
		//Scanner sc;
		if (args.length > 0 && args[0].equals("1"))   sc = new Scanner(new File("./input_term.txt"));
		else   										  sc = new Scanner(System.in);

		env.putAll(System.getenv());//didnt want ot do this here needs throws

		add_primary_envvars();
		//getenv doesnt fetch pwd oldpwd

		if (args.length > 0 && args[0].equals("-i"))
				env.clear();

		get_exec_dirs();
		
		String input_line;
		run : while (true)
		{
			cmds.clear();
			System.out.print(c.KGRN +  System.getProperty("user.name") + " MINISHELL [" + cur_path.getCanonicalPath() +  "]\n$" + c.KNRM);	
			input_line = sc.nextLine();//all whitespaces //VERY IMMPORT TO OELIMINATE EXTRA SPACES AND TABS find replaceall regex tabs and spaces
			
			history.add(input_line);
			Files.write(Paths.get(System.getProperty("user.dir") + "/history.txt"), ("\n" + input_line).getBytes(), StandardOpenOption.APPEND);
			
			get_input_lines(input_line);

			if (input_line.length() > 0)//if enter do nothing
				stock_in_cmds(null);
			
			//display errors first than good
			//sort false than rights
			
			
			cmds.sort((cmd1, cmd2) -> cmd1.found.compareTo(cmd2.found));
//display_cmds();
			//for (Command cmd : cmds)
			for (int i = 0; i < cmds.size(); i++) 
			{
				launch_command(cmds.get(i));
				if (exit_shell)
					break run;
			}
			
		}

		System.out.println("----------------- leaving shell -------------");
		//System.out.println(/* text */);
		//System.out.println(get_cmd("exit"));
		//display_cmds();
		//display_env(5);
		//display_builtcomm();
		
		
		sc.close();

	}
}






