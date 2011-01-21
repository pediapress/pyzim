#include <zim/blob.h>
#include <zim/writer/articlesource.h>
#include <zim/writer/zimcreator.h>


class PyArticle: public zim::writer::Article {
public:
	PyArticle(const std::string& url, const std::string& title, const std::string& aid)
		: url_(url), title_(title), aid_(aid) {}

	std::string getAid() const {
		return aid_;
	}

	char getNamespace() const {
		return 'A';
	}

	std::string getUrl() const {
		return url_;
	}

	std::string getTitle() const {
		return title_;
	}

	bool isRedirect() const {
		return false;
	}

	std::string getMimeType() const {
		return "text/html";
	}

	std::string getRedirectAid() const {
		return "";
	}

private:
	std::string url_;
	std::string title_;
	std::string aid_;
};


class PyArticleSource: public zim::writer::ArticleSource {
public:
	PyArticleSource() : count_(0) {}

	void push_back(const PyArticle* article) {
		articles_.push_back(article);
	}

	virtual const zim::writer::Article* getNextArticle() {
		if (count_ < articles_.size()) {
			return articles_[count_++];
		}
		return 0;
	}

	zim::Blob getData(const std::string& aid) {
		std::cerr << "get_data" << aid << std::endl;
		return zim::Blob(" ",1);  // XXX
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
