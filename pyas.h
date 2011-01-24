#include <zim/blob.h>
#include <zim/writer/articlesource.h>
#include <zim/writer/zimcreator.h>

#include <algorithm>


class PyArticle: public zim::writer::Article {
public:
	PyArticle(char ns, const std::string& url, const std::string& title,
		  const std::string& aid, const std::string& redirectAid,
		  const std::string& mimetype)
		: namespace_(ns),
		  url_(url),
		  title_(title),
		  aid_(aid),
		  redirectAid_(redirectAid),
		  mimetype_(mimetype) {
	}

	std::string getAid() const {
		return aid_;
	}

	char getNamespace() const {
		return namespace_;
	}

	std::string getUrl() const {
		return url_;
	}

	std::string getTitle() const {
		return title_;
	}

	bool isRedirect() const {
		return !redirectAid_.empty();
	}

	std::string getMimeType() const {
		return mimetype_;
	}

	bool shouldCompress() const {
		return mimetype_ == "text/html";
	}

	std::string getRedirectAid() const {
		return redirectAid_;
	}

	void setData(const std::string& data) {
		data_ = data;
	}

	zim::Blob getData() const {
		return zim::Blob(data_.c_str(), data_.length());
	}

private:
	char namespace_;
	std::string url_;
	std::string title_;
	std::string aid_;
	std::string redirectAid_;
	std::string mimetype_;
	std::string data_;
};


class AidCmp {
public:
	AidCmp(const std::string& aid) : aid_(aid) {}
	bool operator()(const PyArticle* article) {
		return aid_ == article->getAid();
	}

private:
	const std::string& aid_;
};


class PyArticleSource: public zim::writer::ArticleSource {
public:
	PyArticleSource() : count_(0) {}

	void addArticle(const PyArticle* article) {
		articles_.push_back(article);
	}

	virtual const zim::writer::Article* getNextArticle() {
		if (count_ < articles_.size()) {
			return articles_[count_++];
		}
		return 0;
	}

	zim::Blob getData(const std::string& aid) {
		std::vector<const PyArticle*>::const_iterator it;
		it = std::find_if(articles_.begin(), articles_.end(), AidCmp(aid));
		return (*it)->getData();
	}

private:
	std::vector<const PyArticle*> articles_;
	int count_;
};


void create(const std::string& fname, PyArticleSource* src) {
	int argc = 0;

	try {
		zim::writer::ZimCreator creator(argc, (char**)0);
		creator.create(fname, *src);
	}
	catch (std::exception& e) {
		std::cerr << "exception called:" << e.what() << std::endl;
	}
}
