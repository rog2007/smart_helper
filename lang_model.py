from llama_cpp import Llama
import socket, argparse

SYSTEM_PROMPT = "Ты — русскоязычный автоматический ассистент. Ты помогаешь структурировать ответы."
SYSTEM_TOKEN = 1788
USER_TOKEN = 1404
BOT_TOKEN = 9225
LINEBREAK_TOKEN = 13

ROLE_TOKENS = {
    "user": USER_TOKEN,
    "bot": BOT_TOKEN,
    "system": SYSTEM_TOKEN
}


def get_message_tokens(model, role, content):
    message_tokens = model.tokenize(content.encode("utf-8"))
    message_tokens.insert(1, ROLE_TOKENS[role])
    message_tokens.insert(2, LINEBREAK_TOKEN)
    message_tokens.append(model.token_eos())
    return message_tokens


def get_system_tokens(model):
    system_message = {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
    return get_message_tokens(model, **system_message)


def interact(
    model_path="./model-q4_K.gguf",
    n_ctx=2000,
    top_k=30,
    top_p=0.9,
    temperature=0.2,
    repeat_penalty=1.1,
    mainSock=1488
):

    model = Llama(
        model_path=model_path,
        n_ctx=n_ctx,
        n_parts=1,
        #n_gpu_layers=-1
    )

    system_tokens = get_system_tokens(model)
    tokens = system_tokens
    model.eval(tokens)

    sock = socket.socket()
    curSock = 1488
    for trySock in range(1488, 1588):
        print(trySock)
        try:
            curSock = trySock
            sock.bind(('', trySock))
            break
        except Exception:
            pass
    sock.listen(1)

    newSock = socket.socket()
    newSock.connect(("localhost", mainSock))
    newSock.send(str(curSock).encode())
    newSock.close()

    conn, addr = sock.accept()

    while True:
        user_message = conn.recv(1024).decode()
        if user_message == "!!!close!!!":
            newSock.close()
        if not user_message:
            continue
        message_tokens = get_message_tokens(model=model, role="user", content=user_message)
        role_tokens = [model.token_bos(), BOT_TOKEN, LINEBREAK_TOKEN]
        tokens += message_tokens + role_tokens
        generator = model.generate(
            tokens,
            top_k=top_k,
            top_p=top_p,
            temp=temperature,
            repeat_penalty=repeat_penalty
        )
        for token in generator:
            token_str = model.detokenize([token]).decode("utf-8", errors="ignore")
            tokens.append(token)
            if token == model.token_eos():
                break
            conn.send(token_str.encode())
        conn.send("!!!end_phrase!!!".encode())


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-s", "--socket")
    args = argParser.parse_args()
    interact(mainSock=int(args.socket))
