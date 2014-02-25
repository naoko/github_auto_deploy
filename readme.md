inspired by Github-Auto-Deploy


Motivation:
----
our servers are only accessible via VPN and auto deployment from CI SaaS wasn't an option for us.

What this does:
---
This is a simple HTTP server that receive commit info from github and deploy app to servers with your faborite script (bash, fabric, saltstack)

It also provides nice logging and security

In our shop, once code is pushed, codeship will run tests and coverall will check code coverage etc...

Then manual code review is done by human and reviewer will merge the code to master

Once code is merged to master, we were running fabric script to deploy. This is the part we wanted to automate and this code I hope to help faciliate that.

How it works:
---
You can set up [Post-Receive Hooks](https://help.github.com/articles/post-receive-hooks "Post-Receive Hooks") on github.
Whenever the repository is pushed, it post repo info (shown below) to this auto deploy server and run your deploy script.

<pre>
{
  :before     => before,
  :after      => after,
  :ref        => ref,
  :commits    => [{
    :id        => commit.id,
    :message   => commit.message,
    :timestamp => commit.committed_date.xmlschema,
    :url       => commit_url,
    :added     => array_of_added_paths,
    :removed   => array_of_removed_paths,
    :modified  => array_of_modified_paths,
    :author    => {
      :name  => commit.author.name,
      :email => commit.author.email
    }
  }],
  :repository => {
    :name        => repository.name,
    :url         => repo_url,
    :pledgie     => repository.pledgie.id,
    :description => repository.description,
    :homepage    => repository.homepage,
    :watchers    => repository.watchers.size,
    :forks       => repository.forks.size,
    :private     => repository.private?,
    :owner => {
      :name  => repository.owner.login,
      :email => repository.owner.email
    }
  }
}
</pre>



How to set it up:
---
1. Install auto deploy server
<pre>
git https://github.com/naoko/github-auto-deploy.git
cd github-auto-deploy
pip install -r requirements.txt
python deploy-server.py
</pre>

2. Test (optional)
setup post-receive hooks. You can test webhooks by following [this instrcution](https://help.github.com/articles/testing-webhooks). Paste raw
<pre> curl -i -d 'payload=xxxx'</pre>

3. in fabfile, moidfy env.hosts and env.user
4. generate ssh key on server
4. copy public key to server. you can use push_pub_key in fabfile. This command will copy local public key to ~/.ssh/authorized_keys on server.
<pre>fab push_pub_key</pre>


Security:
---
 * Currently it checks to see if request IP is from github
 * We recommend to use HTTPS for webhook
 * 

to do:
---
more security

naoko rock! yep that's right!

fefe  fefe
dfdfef


