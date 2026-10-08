from boofuzz import *

def main():
	session = Session(
		target = Target(
			connection=SocketConnection(
				"127.0.0.1",
				9999,
				proto="tcp"
			)
		)
	)
	s_initialize("simple_request")
	if s_block_start("request"):
		s_string("HELLO")
		s_delim("|")
		s_string("FUZZ")
		s_block_end()
	
	session.connect(s_get("simple_request"))

	session.fuzz()


if __name__ =="__main__":
	main()
