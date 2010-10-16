#include "zim/writer/articlesource.h"
#include "zim/blob.h"
#include "zim/writer/zimcreator.h"

class PyArticle: public zim::writer::Article
{
public:
	std::string url;
	std::string title;
	std::string aid;
	std::string getAid() const {
		return aid;
	}

	char getNamespace() const {
		return 'A';
	}

	std::string getUrl() const {
		return url;
	}

	std::string getTitle() const {
		return title;
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
};

class PyArticleSource: public zim::writer::ArticleSource
{
public:
	PyArticleSource() {
		count=0;
	}
	virtual const zim::writer::Article* getNextArticle() {
		if (count<articles.size()) {
			return articles[count++];
		}
		return 0;
	}

	zim::Blob getData(const std::string& aid) {
		std::cerr << "get_data" << aid << std::endl;
		return zim::Blob(" ",1);  // XXX
	}

	std::vector<zim::writer::Article *> articles;
	int count;
};

void create(const std::string &fname, PyArticleSource *src)
{
	int argc=0;
	try {
		zim::writer::ZimCreator creator(argc,(char**)0);
		creator.create(fname, *src);
	}
	catch (std::exception &e) {
		std::cerr << "exception called:" << e.what() << std::endl;
	}
}
