---
title: 肖臻-区块链 笔记
categories:
  - Web3
description: "肖臻-区块链学习笔记"
date: 2024-01-23 12:10:40
excerpt: "这是一份肖臻老师的课程笔记，主要讲解了区块链的概念，基本没有什么代码片段，因此也可以当作科普类笔记，但是内容较为干枯"
copyright: 无
tags:
    - 区块链
    - 比特币
    - 以太坊
---

## 工具包

课程链接：【北京大学肖臻老师《区块链技术与应用》公开课】 https://www.bilibili.com/video/BV1Vt411X7JF

区块链demo：https://andersbrownworth.com/blockchain

## 前言

这份网课是为了毕设做准备的，因此特此花费了一些时间用以学习区块链的本质

在这份笔记中，你会了解比特币挖矿的真相，以及矿潮没落的原因

但是比较无语的是，这份课程录制的时候我还在上初中，因此有部分内容可能以及随着时间发生了一些变化，需要辩证看待部分内容的正确性

如果您发现笔记之中不正确的地方，欢迎您为我指正错误，联系方式见**关于**里的邮箱，感激不尽！

## 密码学原理

### 哈希

加密货币实际是不加密的，线上公开透明；以最著名的加密货币比特币为例，它使用的是哈希和数字签名，密码学中的**哈希**被称为**cryptographic hash function**，它有一个特性叫**collision resistance**，也有地方说成**collision free**，但实际上哈希碰撞是不可避免的,这个特性当个玩笑话即可，马马虎虎可以这么认为，但不能当作真理。

**collision resistance**，指的是对于H(x),我们没有办法做到人为高效地找到一个H(x')，使得H(x)==H(x')，通俗易懂一点来说，就是做不到篡改但是不被发现，只要x有一丁点变化，那么最终的哈希值就会与先前有所不同。在Golang的项目依赖管理go.mod和go.sum中有着类似的机制，go.mod存放了项目所需要的依赖，而go.sum则存放了依赖所对应的哈希值，一旦我们在拉取代码并使用go get下载对应依赖时，下载的依赖被人篡改，那么新依赖计算出来的哈希值就会与go.sum中的原依赖哈希值不符，进而引发警告。

**哈希碰撞**，指的是对于x≠y,但是存在H(x)==H(y),使得不同输入会在哈希表被映射到同一个位置。由于哈希的输出空间只有2^256，且输出空间理论上是可以无限大的，因此哈希碰撞不可避免。但是目前来说，对于x，我们并没有高效的方式能够求得y满足哈希碰撞，暴力求解理论上可以完成，但是对于2^256种哈希值，这种方法非常困难。

*//此处H(x)，相当于x的digest,部分论文会将其翻译做摘要，姑且可以当作x的指纹，“独一无二”的标识*

因此，对于哈希函数，必须要严格补充一句，**collision resistance**本身是**无法被证明**且实际是**不可能存在**这种性质的，但是如果一个哈希函数在过去很长一段时间，没有人找到人为高效制造哈希碰撞的方法，我们就默许它是collision resistance的，这属于是一种比较经验化的性质，找不到等于“没有”。当然也有一些哈希函数，在过去是被认为是collision resistance的，但后来被发现可以人为制造哈希碰撞的方法，最为著名的就是MD5加密，以下是在Flask中一段经典的MD5加密代码。

```py
password = hashlib.md5(password.encode()).hexdigest()
```

哈希函数还有一个性质，叫**hiding**，简单来说，哈希函数是单向的，x-->H(x)这个过程是不可逆的，除了蛮力，无法高效地破解,但这有一个前提，哈希的输入范围要足够大且分布要足够均匀，否则也会因为输出范围太过狭隘导致被暴力破解，这一点可以参考《模仿游戏》中阿兰·图灵最后破解德军恩格玛电报的原因。

当collision resistance和hiding结合使用时就可以实现**digital commitment**，有时候也叫**digital equivalent of sealed envelope**。

> 什么是digital commitment？假设现实世界出现了一名法师奇异博士，他在使用了时间宝石之后，能够准确预言未来发生的事情。请问作为旁观者，我们该如何证明他的能力呢？最简单粗暴的办法就是，让他先预言，再等预言的时间到了，看看预言的事情是否发生。这听上去非常合理，但是事实上，一旦预言被公布出来，那么未来就可能会**因为预言被公布这件事**而发生改变。例如，奇异博士预言了古一会死亡，本来按照时间线，古一可能的的确确是会死亡，但是由于奇异博士的预言，导致众人因为保护古一，而使其没有阵亡，或者说因为众人保护古一的过程中出现了意外导致古一阵亡。这无论是哪种情况，都没办法佐证奇异博士的预言能力。因此，我们得出结论，**预言是不可公开的**。我们正确的做法是让奇异博士将预言的内容封死在绝对安全的保险箱中，确保没有人知道预言，待预言的时间到了，再打开确认有没有发送预言中出现的事情。

对于电子世界，我们想要做到类似的事情，我们就需要将内容进行哈希加密，将得出的哈希值公布出去，并将原文内容封锁在digital sealed envelope中，一旦到了需要解密的时候，我们再解开digital sealed envelope，由于哈希函数具有hiding的性质，因此即便公布哈希值也推不出原文，更不会影响未来，而又由于具备collision resistance的性质，如果公布出来的内容和原文不一样或者说被篡改了，那么通过哈希值就可以轻易判断。

实际操作中，为满足hiding性质的前提，我们会对原文尾部添加一串随机数，将两个部分同时进行哈希加密，这样可以确保输入范围大，输出分布均匀，如：”今天看起来是个不错的日子||1018“，其中1018就是拼接的随机数。

另外，在比特币中，还有一个性质，叫**puzzle friendly**，这个说的是，在工作量证明机制中，**挖矿没有捷径**，只能够通过一遍遍地试随机数，使得 Hash ( block,header ) <= target(指定阈值)。值得一提的是，在其中一名矿工成功计算出随机数之后，其他矿工需要去验证这个随机数是否正确，而这个验证方法十分简单，只需要将其重新带回Hash ( block,header ) ，查看结果是否小于等于目标阈值，因为计算复杂，求证简单，因此，这个性质又被称作"difficult to solve, but easy to verify"[难以解决，但容易求证]

比特币中使用的哈希函数叫SHA-256(Secure Hash Algorithm)，它同时具备了上述性质。

![image-20240112095737762](/img/xiaozhen_blockchain_note/image-20240112095737762.png)

![image-20240112095746127](/img/xiaozhen_blockchain_note/image-20240112095746127.png)

上图为哈希加密的一个示例，来源：https://andersbrownworth.com/blockchain/hash

*//这个博主的个人网页也有写有关区块链的内容*



### 数字签名

对于不安全的通信渠道，即便是有了普通的加密措施，也就是对称加密，也可能会因为密钥被截取而导致信息泄露，于是非对称加密应运而生。

**非对称加密**，即使用公钥加密，私钥解密，由于私钥是存放在本地的，并不需要参与通信，因此我们不需要担心在通信过程导致私钥被截取。而公钥是公开的，所有人都可以拿到，它只具备加密的能力，并不能解密，所以不存在公钥被截取导致信息泄露。在通信过程中，我们使用对方的公钥进行加密，对方收到信息之后，会使用本地的私钥进行解密，传输过程中，信息是处于加密状态的。

值得一提的是，公钥是私钥通过某种方法去推算出来的，且这个运算是不可逆的，也就是说，知道私钥的人可以推导出对应的公钥，但知道公钥的人无法逆向推导出私钥。

> 通俗易懂地来说就是，我用我手里的钥匙制作了足够多的锁，我把我的锁发给全世界每个人，他们如果想给我邮寄东西，就必须用我给的锁上锁，上完之后，除了我手里的钥匙，没人能够打开它。这就是非对称加密。

非对称加密技术我们可以用来制作签名，以比特币交易为例，假设LRay向B转了10个比特币，交易产生并且记录被发布到区块链中，其他节点如何认可此次交易的真实性呢？

那么LRay就会在发布交易时，同时发布一个签名（使用私钥加密这个签名），其他节点再使用公钥去验证这个签名的真实性。

> 肖臻：是否存在两个人公钥和私钥一模一样的情况呢？即小黑发起大量攻击，产生大量的公私钥，再检查自身产生的公钥是否和区块链上已有的公钥是否相同，直到产生的某个公钥，恰好能够和用户C的公钥一模一样，这样小黑就得到了用户C的公私钥，那么小黑是否可以使用他的公私钥发布交易，或者篡改用户C的交易呢？
>
> 理论上确实可行，但是实际上，对于256位(二进制，10进制大约78位)的公私钥，出现相同的概率微乎其微，哪怕是超级计算机，日夜兼程计算，找到的概率甚至小于地球爆炸的可能性。但这一且都是建立在有一个良好的随机源的基础上，如果随机源不够优秀，可能会在一遍遍的签名中将私钥破解出来。



## 比特币的数据结构[已废弃，可不学]

![image-20240105091958351](/img/xiaozhen_blockchain_note/image-20240105091958351.png)



### 区块链

*//特奶奶个锤，学了一大半才发现这玩意已经被合并掉了，没话说，日常白学，习惯就好*

区块链本身是有区块组成的链表，和传统的链表有所不同

首先是哈希指针和传统指针有所不同，相比起传统指针p（存放了结构体在内存中的起始地址），增加了一个H(x)，也就是说，哈希指针不仅需要保存地址，还需要保存一个哈希值，这个哈希值可以用来检测结构体中的内容是否被篡改。

![](/img/xiaozhen_blockchain_note/cec260ce36410d64a2e680b87dafbbe.png)

<center>hash pointer，哈希指针</center>

下面是一种简单的区块链结构

![](/img/xiaozhen_blockchain_note/b82daa61a0de14965f383ca4cfbf309.png)

最左边的叫创世区块，是区块链中的第一个区块，之后的每一个区块的都会保存着上一个区块的地址以及哈希值。而最后一个区块的地址和哈希值保存在系统中，一旦中间的某一个区块被篡改，H( )变成了H'( )，那么牵一发而动全身，后面区块的哈希值都会发生变化，最终系统会发现最后一个区块的哈希值与保存的哈希值有所不同。以下是一个范例：

![image-20240115231345044](/img/xiaozhen_blockchain_note/image-20240115231345044.png)

![image-20240115231352791](/img/xiaozhen_blockchain_note/image-20240115231352791.png)

一旦发生篡改

![image-20240115231411208](/img/xiaozhen_blockchain_note/image-20240115231411208.png)

另外这种结构还具备temper-evident log，即可追踪日志，还是以刚才被篡改的区块为例，假如系统中只保存了后两个区块的，我们想要前面的区块中的内容，我们向前面节点发起了请求，我们对发来的区块链中的most recent block进行哈希计算，得到的哈希值如果和我们最老的区块中保存的哈希值不符合，那么就说明发来的数据是有被篡改的。

在比特币中，除了区块链，还有一种结构，叫**Merkle tree**



### Merkle tree

![](/img/xiaozhen_blockchain_note/3f0cfb0ee800495f367fb49c58eea45.png)

<center>Merkle tree</center>

长相上和二叉树有类似的地方，但和二叉树有所不同的是，使用了哈希指针代替了普通指针，子节点中的哈希值存在它们的父节点中，优点是只需要记住最上方根节点的哈希值，就可以检测出merkle tree中任何一个节点是否发生篡改，原理和之前的区块链表有所类似。

**根哈希值存放在block header中，而block body中包含了交易列表**

用途：

比特币中的节点分为轻节点(light node)和全节点(full node)两类，全节点是保存整个区块的内容（block header+block body），而轻节点只保存了block header



### Merkle Proof

Merkle Proof ，用于寻找交易所在的节点路径，查询交易是否被写进区块链中。轻节点中只包括了块头部分，因此，MerkleProof的第一步就是向全节点发送请求，之后全节点会返回一条交易路径和沿途的H(),而轻节点要做的就是对哈希值进行计算，判断最终结果与块头中的根哈希值是否相同。

*//具体见下方肖臻老师的演示课件*

> 以下是肖臻老师PPT所做的演示，是将两种区块链结构合二为一，做的显然更加细致
>
> ![](/img/xiaozhen_blockchain_note/9c36b711da645ebc72e4fb5b73b7572.png)
>
> 这张图片展示了区块链节点中的以部分，每一个区块下存放着一个merkle tree，而树的地步是交易明细，在我们查询交易的时候，为了验证某个交易是否存在，轻节点会先向全节点发送请求，全节点会返回红色部分的哈希值以及交易的路径，轻节点只需要使用底部需要查验的交易哈希值，一步一步推出父节点中的绿色哈希值，知道推出根节点中的哈希值，与块头中的根哈希值进行比对。
>
> *红色的哈希值我们是无法验证的，因为轻节点的这一次查询，只能查询路径中的部分，黑色部分都是无法查询的,我们无法判断红色哈希值的正确性*

这种查询方式也被成为 proof of membership/proof of inclusion,复杂度是θ(log(n))；如果是 proof of non-membership呢？那就是将整个merkle tree都发送给轻节点了，复杂度是θ(n)



## ETH以太坊

#### 机制区别

> 比特币是proof of work（**工作证明机制**）,以太坊是proof of stake（**权益证明机制**）；
>
> *//值得一提的是，比特币和以太坊在2022年已经完成合并，因此先前部分笔记需要进行修改。*
>
> *// 其实有一部分相当于白学了#无能狂怒 #龙怒*

**传统比特币**（现已与以太坊合并），在前面交易中收到的货币，必须要在之后一次性花出去

例如：LRay-iu转给B10个比特币，B要在将来一次性全部交易出去，多余的则成为了tranactions fee

原因：比特币没有基于账户的模型，是对交易进行单独处理的，这个在其数据结构中也能看出一点

而**以太坊**是基于account-based ledger，有着基于账户的模型，因此，完全不需要全部交易，多出来的以太币纠结着存放在账户中，同时也不再需要哈希指针指向上一条交易

而在比特币中需要关心的一个问题--货币的双重支付（double spending attack），在以太坊对这个有着天然的防御作用，但是与之相对的有着另一个问题，重放攻击（reply attack）

> 简单来说，与双重支付相对，重放指的是收钱方存在恶意，比如LRay-iu向B转了10个以太币，而B在收到这10个以太币之后，将这一条交易又广播了一遍，那么LRay-iu的账户可能会被转2次钱。

解决方案，在账户下对应保存账户的交易次数nonce。在发布交易的时候节点也会更新交易次数，以避免重放交易。



#### 智能合约

智能合约是一种在区块链上执行的自动化合约，它是一段以编程方式编写的代码，旨在自动执行、管理或强制执行合同条款或协议。这些合约以代码的形式存在于区块链上，其中包含了特定的规则和逻辑，通过在区块链网络上运行，可以在没有第三方参与的情况下执行交易或协议。

智能合约运行于区块链网络中的节点上，并且由网络中的所有节点来验证和执行，确保了其去中心化和不可篡改性质。

P.S 换句话说，智能合约一经发布，即便是开发者本身也不能修改合约。



#### 合约账户

创建合约会返回一个地址，知道这个地址就可以调用这个合约,调用过程中状态会发生变化。

> **外部账户**：balance（账户余额），nonce（交易次数）
>
> **合约账户**：balance（账户余额），nonce（用来记录，调用其他合约的次数），并不是依赖公私钥进行控制，并且以太坊中有规定，合约账户不可以主动发起交易。code（代码），storage（存储相关状态）



## 以太坊数据结构

对比比特币中的merkle tree并没有提供高效查找和更新的方法

### Trie

Trie 是一种树形结构，由节点和边构成，每个节点代表一个字符（或一个字节）的信息，而边则代表字符之间的关系。Trie 的特点在于利用共享前缀来节省存储空间，提高数据存取的效率。

> 以下是一张经典的Trie图
>
> ![](/img/xiaozhen_blockchain_note/ed5b963beaf85e5b9e489a10efcc51f-170441778579113.png)
>
> 优点：
>
> **高效的数据检索**： Trie 的查找效率取决于key(上述单词的长度)的长度
>
> **不会发生数据碰撞**：不同的地址(key)，映射到树中的位置也注定不同
>
> **不同节点按照不同的顺序插入树中，得到的树的结构是一样的**
>
> **局部更新**： 当区块发生变化，只需要对发生变化的部分进行更新
>
> 缺点：
>
> **存储敏感性：** Trie 数据结构对存储敏感，对于大型区块链，存储 Trie 可能需要大量的存储空间。



### Patricia tree

为了解决占据存储的问题，有了优化过的**Patricia tree** ，也有写作 **Patricia trie **，

> 经过压缩过的树，层数减少，访问内存的次数也减少，从而提高了性能；
>
> 而新加入的词会扩展已经被压缩过的节点
>
> ![](/img/xiaozhen_blockchain_note/04b959cbb244f9b3d13a0cefae513ab.png)



### Merkle Patricia tree

Merkle Patricia tree (MPT),所有账户组织成一张Patricia tree，用路径压缩，再将指针替换成哈希指针，最后计算出状态树根节点的哈希值，写在block header中。

### 状态树

P.S 以太坊中的账户地址一般是160位的，也就是20个字节，通常表示成40个16进制数字

![](/img/xiaozhen_blockchain_note/5d552b84a412de924d855c63a4498a7.png)

<center>以太坊状态树，来源：肖臻老师PPT</center>

值得一提的是，状态树的更新并不会在原处修改，而是会另开一个区块；

**原因**：以太坊由于有智能合约存在，不能像比特币那样随意回滚



## 交易树-

**作用：**

- 提供merkle proof
- 查找过去一段时间与某个智能合约有关的交易

交易树中包含了这个区块中的所有交易，并且可以通过**bloom filter**快速查找交易是否存在。



#### bloom filter

用于查找交易，存放在块头中，在以太坊中将交易映射至一张表之中，在查找交易的时候，只需要将交易哈希处理后，在表中查找对应位置是否为1；之后在根据结果判断是否需要向全节点查询更详细的内容



### 收据树

收据树存储了每个区块中交易的收据（receipts）。交易执行完成后，会生成一个收据，记录了交易的执行结果、日志、事件等信息。这些收据包含了交易的详细信息，例如合约的调用结果、Gas消耗、事件日志等。

收据树的根哈希值也被包含在区块头中，因此可以通过区块头的根哈希验证交易的有效性，并且可以快速检索特定交易的执行结果。



### 总结

状态树中保存的是(key,value)

用RLP（Recursive Length Prefix）作序列化之后再存储，涉及库（Protobuf 只支持一种类型：nested array of bytes字符数组)

它和交易树、收据树的区别是它包含了系统中所有账户的状态，无论这个账户是否参与了当前区块的交易。

> [^肖臻]: **提问**
>
> **有没有可能A向B转了10ETH，但是B这个账户以前从来没听说过？**
>
> 答：存在，以太坊中，创建账户是不需要通知其他人的，只有这个账户第一次产生交易，其他节点才会知道这个账户存在，这个时候会在状态树中新加入一个账户。
>
> **可以将状态树设计修改成每个区块的状态树只包含这个区块中相关交易的账户？**
>
> 答：这会导致没有任何一个区块保存了完整的状态树，当我们查找状态信息时需要一节一节地去上一个区块中查找对应账户的状态信息，假如这个账户许久没有发生交易，那么，这个查询过程会需要花费很久，甚至会追溯至创世区块。
>
> 更大地问题是，假如回到上一个问题中，A向B转了10个ETH，但假如B这个账户是刚刚建立的，那么其他节点在查找这个账户的时候，会一直查找上一个区块，直到创世区块之后才能够得知B账户是新建的

//*以太坊数据结构的代码此处暂时省略（看不懂），等之后看懂了再补充在这里*

```go
//以太坊交易树和收据树树数据结构
//block.go
```



## ETH以太坊--智能合约

智能合约本质是运行在区块链上的一段代码，代码的逻辑定义了合约的内容，语言是solidity，语法上和js接近。

*//这块没听懂，我暂且先跳过了*

*//当然是因为我太笨了，不过如果你和我一样笨的话，建议别看他讲的*
